from courant.core.dynamic_models.models import DynamicModelBase, DynamicType

from django.contrib.contenttypes.models import ContentType
from django.db.models.base import Model
from django.db.models.signals import post_save, post_delete

class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model for get tag more than once.
    """
    pass

class GetTag(object):
    def __init__(self):
        self._registry = {}
        self._plural_names = {}
        self._singular_names = {}

    def register(self, model, name_field='name',
                 singular_name=None, plural_name=None,
                 with_func=None, in_func=None,
                 filter_func=None):
        """
        Sets the given model class up for working with tags.
        """
        if model in self._registry:
            raise AlreadyRegistered(
                _('The model %s has already been registered.') % model.__name__)
            
        opts = {'name': name_field,
                'with': with_func,
                'in': in_func,
                'filter': filter_func}
        
        pname = unicode(model._meta.verbose_name_plural).lower().replace(' ', '_')
        sname = unicode(model._meta.verbose_name).lower().replace(' ', '_')
        self._plural_names[(plural_name or pname)] = model
        self._singular_names[(singular_name or sname)] = model
        
        self._registry[model] = opts
        
        # auto-register any existing dynamic model configurations of this model
        if issubclass(model, DynamicModelBase):
            self._registry[model]['is_dynamic'] = True
            self._registry[model]['non_dynamic_names'] = [sname, pname]
            self.update_dynamic_registrations(model)

    def unregister(self, model):
        if model in self._registry:
            del self._registry[model]
            for name in self._plural_names.keys():
                if self._plural_names[name] == model:
                    del self._plural_names[name]
            for name in self._singular_names.keys():
                if self._singular_names[name] == model:
                    del self._singular_names[name]
    
    def from_name(self, name):
        name = name.lower()
        if name in self._plural_names:
            return self._plural_names[name]
        elif name in self._singular_names:
            return self._singular_names[name]
        return None

    def from_model(self, model):
        return self._registry.get(model, None)
        
    def update_dynamic_registrations(self, model):
        if issubclass(model, DynamicModelBase): #sanity check
            self._registry[model]['dynamic_map'] = {}
            dTypes = DynamicType.objects.filter(base=ContentType.objects.get_for_model(model))
            for dType in dTypes:
                sname =dType.name.lower().replace(' ', '_')
                pname = dType.name_plural.lower().replace(' ', '_')
                self._plural_names[pname] = model
                self._singular_names[sname] = model
                self._registry[model]['dynamic_map'][sname] = dType.pk
                self._registry[model]['dynamic_map'][pname] = dType.pk

gettag = GetTag()

def update_dynamic_model_registrations(sender, instance, **kwargs):
    gettag.update_dynamic_registrations(instance.base.model_class())
post_save.connect(update_dynamic_model_registrations, sender=DynamicType)

def remove_dynamic_model_registration(sender, instance, **kwargs):
    del gettag._singular_names[instance.name.lower().replace(' ', '_')]
    del gettag._plural_names[instance.name_plural.lower().replace(' ', '_')]
post_delete.connect(remove_dynamic_model_registration, sender=DynamicType)