from django.template import Library, Node, Variable, TemplateSyntaxError, VariableDoesNotExist
from django.template.loader import get_template
from django.conf import settings
from django.db.models.loading import get_model
from django.db.models.fields.related import ManyToManyRel
from django.db.models import Count
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_unicode

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from courant.core.news.models import Section
from courant.core.utils.text import split_contents

from datetime import timedelta, datetime, date

from tagging.models import Tag, TaggedItem

register = Library()

def parse_string_variable(value, context):
   bools = { 'True': True, 'False': False }
   if value in bools:
      return bools[value]
   else:
      return Variable(value).resolve(context)

class RenderNode(Node):
   def __init__(self, template, params):
      self.template = template
      self.params = params
      
   def render(self, context):
      try:
         template_bits = self.template.split('+')
         template = get_template(''.join([Variable(bit).resolve(context) for bit in template_bits]))
         
         # we only want the template to be rendered to see the parameters,
         # so we need to track which context variables we added so we can
         # remove them after the template is rendered
         changelist = {}
         for key, value in self.params.items():
            changelist[key] = context.get(key, None) # store current value, if any
            context[key] = parse_string_variable(value, context)
         t = template.render(context)
         for key, value in changelist.items():
            if value:
               context[key] = value # return to old value
            elif key in context:
               try:
                  del(context[key]) # delete value altogether
               except:
                  pass
         return t
      except TemplateSyntaxError, e:
         #if settings.TEMPLATE_DEBUG:
            raise
         #return ''
      except:
         raise
         #return '' # don't know what's happening, fail silently
   
def do_render(parser, token):
   """
   Loads a template and renders it with the current context plus any passed
   parameters.
   
   The template name can be a concatenation of values by using a
   plus-sign ('+') delimiter. Note that there cannot be spaces between the
   values and the plus sign(s).
   
   Examples::
      
      {% render "foo/some_include.html" %}
      {% render "foo/some_include.html" foo=4 bar="hello world" zed=somevariable %}
      {% render somevar+".html" foo=4 %}
      {% render "test-"+somevar+".html" bar="hello world" %}
   """
   bits = split_contents(token)
   
   params = {}
   if len(bits) > 1:
      param_bits = bits[2:]
      for param in param_bits:
         subbits = param.split('=')
         if len(subbits) != 2:
            raise TemplateSyntaxError, "render parameters must be in name=value format"
         params[subbits[0]] = subbits[1]
         
   return RenderNode(bits[1], params)
register.tag('render', do_render)

class DefaultNode(Node):
   def __init__(self, varname, value):
      self.varname = varname
      self.value = value
      
   def render(self, context):
      if not self.varname in context:
         context[self.varname] = parse_string_variable(self.value, context)
      return ''
   
def do_default(parser, token):
   """
   Sets a context variable to a default value if the variable is currently
   undefined.
   
   Examples::
   
      {% set_default showPhoto True %}
      {% set_default width 250 %}
      {% set_default name "John Smith" %}
   """
   bits = split_contents(token)
   if len(bits) != 3:
      raise TemplateSyntaxError, "set_default: Invalid template tag parameters."
   return DefaultNode(bits[1], bits[2])
register.tag('set_default', do_default)
     
class SettingNode(Node):
   def __init__(self, setting, varname):
      self.setting, self.varname = setting, varname
   
   def render(self, context):
      try:
         setting = settings.__getattr__(self.setting)
      except:
         setting = None
         
      if self.varname:
         context[self.varname] = setting
         return ''
      else:
         return setting
 
def settings_get_setting(parser, token):
   bits = token.contents.split()
   if len(bits) == 2 or len(bits) == 4:
      if len(bits) == 4 and bits[2] != 'as':
         raise TemplateSyntaxError, "second argument to settings_get_settings tag must be 'as'"
      
      if len(bits) == 2:
         varname = None
      else:
         varname = bits[3]
      return SettingNode(bits[1], varname)
   else:
      raise TemplateSyntaxError, "settings_get_settings tag takes exactly one or three arguments"
settings_get_setting = register.tag(settings_get_setting)

class FirstOfNode(Node):
   def __init__(self, vars, varname=None):
      self.vars = map(Variable, vars)
      self.varname = varname
   
   def render(self, context):
      for var in self.vars:
         try:
            value = var.resolve(context)
         except VariableDoesNotExist:
            continue
         if value:
            if self.varname:
               context[self.varname] = value
               return u''
            return smart_unicode(value)
      return u''

def firstof(parser, token):
   """
   Outputs the first variable passed that is not False.
   
   Outputs nothing if all the passed variables are False.
   
   Sample usage::
   
      {% firstof var1 var2 var3 %}
   
   This is equivalent to::
   
      {% if var1 %}
           {{ var1 }}
      {% else %}{% if var2 %}
           {{ var2 }}
      {% else %}{% if var3 %}
           {{ var3 }}
      {% endif %}{% endif %}{% endif %}
   
   but obviously much cleaner!
   
   You can also use a literal string as a fallback value in case all
   passed variables are False::
   
      {% firstof var1 var2 var3 "fallback value" %}
       
   
   Courant addition: Use 'as VARNAME' to save in a variable instead of output
   
      {% firstof var1 var2 var3 as var %}
   """
   bits = token.split_contents()[1:]
   if len(bits) < 1:
      raise TemplateSyntaxError("'firstof' statement requires at least one argument")
   if len(bits) >= 4 and bits[-2] == 'as':
      return FirstOfNode(bits[:-2], bits[-1])
   return FirstOfNode(bits)
firstof = register.tag(firstof)
   

def google_analytics(account=None):
   #If no account is passed in, try and get it from settings
   if not account:
      account = settings.GOOGLE_ANALYTICS_ID;
      #If still not account
      if not account:
         return ''
   
   #Return the JavaScript code, double % signs because of string formatting
   return """
   <script type="text/javascript">
      var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
      document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));
      </script>
      <script type="text/javascript">
      var pageTracker = _gat._getTracker("%(account)s");
      pageTracker._initData();
      pageTracker._trackPageview();
   </script>
   """ % { 'account': account }
register.simple_tag(google_analytics)