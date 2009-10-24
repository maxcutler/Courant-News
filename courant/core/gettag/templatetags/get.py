from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.template.loader import get_template
from django.conf import settings
from django.db.models.loading import get_model
from django.db.models.fields.related import ManyToManyRel
from django.db.models import Count
from django.db.models.query import QuerySet
from django.db.models.manager import Manager
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from courant.core.utils.text import split_contents
from courant.core.gettag import gettag
from courant.core.dynamic_models.models import DynamicType

from datetime import timedelta, datetime, date

register = Library()

def model_from_name(name):
    model = gettag.from_name(name)
    if not model:
        raise TemplateSyntaxError, "Invalid model provided: %s" % name
    return model

def resolve_param(value, context, func=str):
   """
   Resolves a variable passed to a template tag if it exists in the request's
   context. Otherwise applies a specified function to convert it to the desired
   object type (e.g., string or integer)
   """
   if value in context:
      return Variable(value).resolve(context)
   return func(value)

def model_relationship_field(model, fk_model):
    for field in model._meta.fields:
        if hasattr(field, 'rel') and hasattr(field.rel, 'to'):
            if field.rel.to == fk_model:
                return field.name
    for f, m in model._meta.get_all_related_m2m_objects_with_model():
        if f.model == fk_model:
            return f.get_accessor_name()
    return None

class GetNode(Node):
   def __init__(self, params, varname):
      self.params = params
      self.varname = varname
      
   def render(self, context):
      # determine desired object type
      try:
         model = model_from_name(self.params['app_model'])
      except TemplateSyntaxError:
         model = model_from_name(Variable(self.params['app_model']).resolve(context))
      model_name = model.__name__.lower()
      
      # Base queryset to filter on
      manager = model.live if hasattr(model, 'live') and isinstance(model.live, Manager) else model.objects
      opts = gettag.from_model(model)
      if opts.get('is_dynamic', False) and model_name not in opts.get('non_dynamic_names', ''):
         dType = DynamicType.objects.get(pk=gettag.from_model(model).get('dynamic_map').get(model_name, None))
         q = manager.filter(dynamic_type=dType)
      else:
         q = manager.all()
      
      # flag to mark if a value was set before reaching the end of the render
      # function because of a special case
      valueSet = False
      
      # handle with clause
      if 'with_field' in self.params:
         field = self.params['with_field']
         
         # allow custom function to handle with clause for this model type
         custom_with = gettag.from_model(model).get('with', None)
         if callable(custom_with):
            cfield = Variable(self.params['with_field']).resolve(context)

            if 'with_value' in self.params:
               cvalue = Variable(self.params['with_value']).resolve(context)
               result = custom_with(cfield, cvalue)
            else:
               result = custom_with(cfield)
            
            if isinstance(result, QuerySet):
               # if the function returned a queryset, then we can continue on
               q = result
            else:
               # otherwise just return the value
               context[self.varname] = result
               return ''
         else:
            if not field in model._meta.get_all_field_names():
               raise TemplateSyntaxError, "get tag: field '%s' does not exist on model %s" % (field, model.__name__)
            elif 'with_value' in self.params and isinstance(model._meta.get_field(field).rel, ManyToManyRel):
               raise TemplateSyntaxError, "get tag: cannot match a value to m2m field '%s' on model %s" % (field, model.__name__)
            
            filter_params = {}
            if 'with_value' in self.params:
               # can only resolve a variable value or a quoted string,
               # but users could put an unquoted string/non-variable,
               # so we catch that exception and move on
               try:
                  value = Variable(self.params['with_value']).resolve(context)
               except VariableDoesNotExist:
                  value = self.params['with_value']
                  if value == 'None':
                     value = None

               filter_params[str(field)] = value
            else:
               # only return results that have matching related objects
               # pk > 0 is a hack, as annotations/aggregations are not fast enough
               # (difficult to index properly + complicated joins)
               filter_params[str("%s__pk__gt" % field)] = 0
            q = q.filter(**filter_params)
      
      # handle 'in' clause(s)
      if 'in' in self.params:
         stack = [model]
         filter_params = {}
         exclude_params = {}
         for clause in self.params['in']:
            
            # if the provided type isn't in the map, try to resolve it as a variable
            if gettag.from_name(clause['type']):
               ctype = clause['type']
            else:
               try:
                  ctype = Variable(clause['type']).resolve(context)
                  if isinstance(ctype, int):
                     ctype = ContentType.objects.get(id=ctype_id)['name']
               except VariableDoesNotExist:
                  ctype = clause['type']

            type_model = model_from_name(ctype)
            stack.append(type_model)
            
            # can only resolve a variable value or a quoted string,
            # but users could put an unquoted string/non-variable,
            # so we catch that exception and move on
            try:
               value = Variable(clause['obj']).resolve(context)
               value_in_context = True
            except VariableDoesNotExist:
               value = clause['obj']
               value_in_context = False
               
            # allow for a custom function to handle this clause for this model type
            custom_in = gettag.from_model(gettag.from_name(ctype)).get('in', None)
            if callable(custom_in):
               result = custom_in(q, value)
               if isinstance(result, QuerySet):
                  q = result
                  continue
               else:
                  context[self.varname] = result
                  return ''
            
            # try to find the related field
            related_field = ''
            is_virtual = False
            for m in reversed(stack[:-1]):
               rf = model_relationship_field(m, type_model)
               if rf:
                  if related_field:
                     related_field = '%s__%s' % (rf, related_field)
                  else:
                     related_field = rf
                  type_model = m # track relationship backwards
               
            # if we didn't find a related field...
            if not related_field and len(model._meta.virtual_fields) == 0:
               raise TemplateSyntaxError, "get tag: invalid parameter in 'in %s %s' clause" % (ctype, clause['obj'])
            elif len(model._meta.virtual_fields) > 0:
               is_virtual = True
               filter_params[model._meta.virtual_fields[0].ct_field] = ContentType.objects.get_for_model(type_model).id
               related_field = model._meta.virtual_fields[0].fk_field
            
            # if this is a list of only one value (e.g., from a previous limit 1 call),
            # then we want the object itself
            # we split 'obj' clause in case the passed value is a member of the context variable
            if value_in_context and isinstance(value, list) and len(value) == 1:
               value = value[0]
            
            # if this type has a callable name field, apply it
            field_name = gettag.from_model(gettag.from_name(ctype)).get('name')
            if callable(field_name) and not isinstance(value, type_model):
               value = field_name(value)
            
            # if this type has a filter set, apply it
            filter_func = gettag.from_model(gettag.from_name(ctype)).get('filter', None)
            if filter_func:
               f = filter_func(value)
               related_field = '%s__%s' % (related_field, f[0])
               value = f[1]
            # otherwise, if there is not filter and it wasn't in the context,
            # then we need to suffix the appropriate field name
            elif clause['obj'] not in context:
               related_field = '%s__%s' % (related_field, field_name)
            
            if not is_virtual:
               if clause['exclude']:
                  exclude_params[related_field] = value
               else:
                  filter_params[related_field] = value
            else:
               if clause['exclude']:
                  exclude_params[related_field] = value
               else:
                  filter_params[related_field] = str(value.pk)

         q = q.exclude(**exclude_params)
         q = q.filter(**filter_params)
      
      # handle 'from last' clause
      if 'from_side' in self.params and 'from_timeperiod' in self.params:
         latest_field = model._meta.get_latest_by
         if not latest_field:
            raise TemplateSyntaxError, "get tag: %s does not support 'from last' clause" % model_name
         latest_field = latest_field.strip('-') # remove a minus sign if necessary
         
         if self.params['from_side'] == 'last':
            start = date.today() - timedelta(**{self.params['from_timeperiod']: int(self.params['from_x']) })
            end = date.today() + timedelta(days=1)
         elif self.params['from_side'] == 'next':
            start = date.today()
            end = date.today() + timedelta(**{self.params['from_timeperiod']: int(self.params['from_x']) })
         else: # == 'week'
            if self.params['from_timeperiod'] == 'today':
               day = date.today()
            else:
               day = resolve_param(self.params['from_timeperiod'], context)
               if not (isinstance(day, datetime) or isinstance(day, date)):
                  day = resolve_param(self.params['from_timeperiod'], context, func=datetime)
            offset = datetime.isoweekday(day) % 7 #sunday is first day of week
            start = day + timedelta(-offset)
            end = day + timedelta(7-offset-1)
         p = { '%s__range' % latest_field: (start, end)}
         q = q.filter(**p)
      
      # handle 'order by' clause
      if 'order_by' in self.params:
         order_by = resolve_param(self.params['order_by'],context, str)
         q = q.order_by(order_by)
      
      # handle 'limit' clause
      if 'limit' in self.params:
         limit = resolve_param(self.params['limit'], context, int)
         
         # handle optional 'offset' clause
         if 'offset' in self.params:
            offset = resolve_param(self.params['offset'], context, int)
            q = q[offset:offset+limit]
         else:
            q = q[:limit]    
      
         # if only one object was requested, then don't return a list
         if limit == 1:
            context[self.varname] = q[0]
            valueSet = True
      
      # if the value wasn't set previously in this function
      if not valueSet:
         context[self.varname] = q
      return ''
   
class GetByNameNode(Node):
   def __init__(self, params, varname):
      self.params = params
      self.varname = varname
      
   def render(self, context):
      # determine desired object type
      model = model_from_name(self.params['app_model'])
      
      names = self.params['names']
      objs = []
      for name in names:
         model_name_field = gettag.from_model(model).get('name')
         name = Variable(name).resolve(context)
         #assert False, gettag.from_model(model)
         if callable(model_name_field):
            objs.append(model_name_field(name))
         else:
            p = {model_name_field: name}
            objs.append(model.objects.get(**p))
      
      if len(objs) == 1:
         context[self.varname] = objs[0]
      else:
         context[self.varname] = objs
      return ''

def do_get(parser, token):
   # prepare our data structures
   bits = split_contents(token)
   params = {}
   varname = None
   keywords = ['with','from','in','order','limit','offset']
   
   # remove the template tag name from the bits list
   bits.pop(0)
   
   # check that we have been provided with the desired variable name
   # before doing all the parsing
   if bits[-2] == "as":
      varname = bits.pop()
      bits.pop()
   else:
      raise TemplateSyntaxError, "get tag: must end tag with 'as <varname>'"
   
   # check that some parameters were passed
   if len(bits) < 2:
      raise TemplateSyntaxError, "get tag: the content type and at least one parameter are required"
   
   params['app_model'] = bits.pop(0)
   
   # form 2
   if bits and bits[0] not in keywords:
      params['names'] = bits
      return GetByNameNode(params, varname)
   
   # with clause
   if bits and bits[0] == "with":
      bits.pop(0)
      if len(bits) >= 2 and bits[1] not in keywords:
         params['with_field'] = bits.pop(0)
         params['with_value'] = bits.pop(0)
      elif len(bits) >= 1:
         params['with_field'] = bits.pop(0)
      else:
         raise TemplateSyntaxError, "get tag: invalid syntax in 'with' clause; must be in form 'with <field> <value>' or 'with <m2m_field>'"
   
   # in clauses
   while bits and (bits[0] == "in" or (bits[0] == "not" and bits[1] == "in")):
      if 'in' not in params:
         params['in'] = []
      if bits[0] == "not":
         exclude = True
         bits.pop(0)
      else:
         exclude = False
      bits.pop(0)
      if len(bits) >= 2:
         params['in'].append({
            'type': bits.pop(0),
            'obj': bits.pop(0),
            'exclude': exclude
         })
      else:
         raise TemplateSyntaxError, "get tag: invalid syntax in 'in' clause; must be in form '(not) in <type> <object>'"
   
   # from last clause
   if bits and bits[0] == "from":
      bits.pop(0)
      if len(bits) >= 3 and (bits[0] == "last" or bits[0] == "next" or bits[0] == "week"):
         params['from_side'] = bits.pop(0)
         params['from_x'] = bits.pop(0)
         params['from_timeperiod'] = bits.pop(0)
      else:
         raise TemplateSyntaxError, "get tag: invalid syntax in 'from last' clause; must be in form 'from last <#> <timeperiod>'"
         
   # order by clause
   if bits and bits[0] == "order":
      bits.pop(0)
      if len(bits) >= 2 and bits[0] == "by":
         bits.pop(0)
         params['order_by'] = bits.pop(0)
         if params['order_by'] in keywords:
            raise TemplateSyntaxError, "get tag: invalid syntax in 'order by' clause. must be in form 'order by <field>'"
      else:
         raise TemplateSyntaxError, "get tag: invalid syntax in 'order by' clause; must be in form 'order by <field>'"
      
   # limit ... offset clause
   if bits and bits[0] == "limit":
      bits.pop(0)
      
      if len(bits) >= 1:
         params['limit'] = bits.pop(0)
         if params['limit'] in keywords:
            raise TemplateSyntaxError, "get tag: invalid syntax in 'limit' clause. must be in form 'limit <number>'"
      else:
         raise TemplateSyntaxError, "get tag: invalid syntax in 'limit' clause. must be in form 'limit <number>'"
      
      # optional offset clause
      if bits and bits[0] == "offset":
         bits.pop(0)
         
         if len(bits) >= 1:
            params['offset'] = bits.pop(0)
            if params['offset'] in keywords:
               raise TemplateSyntaxError, "get tag: invalid syntax in 'offset' clause. must be in form 'offset <number>'"
         else:
            raise TemplateSyntaxError, "get tag: invalid syntax in 'offset' clause. must be in form 'offset <number>'"
         
   if bits and bits[0] == "offset":
      raise TemplateSyntaxError, "get tag: 'offset' must follow a 'limit' value"
         
   return GetNode(params, varname)
register.tag('get',do_get)