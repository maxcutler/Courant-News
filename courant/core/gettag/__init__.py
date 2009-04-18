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
        self._registry[model] = opts
        pname = unicode(model._meta.verbose_name_plural).lower().replace(' ', '_')
        sname = unicode(model._meta.verbose_name).lower().replace(' ', '_')
        self._plural_names[(plural_name or pname)] = model
        self._singular_names[(singular_name or sname)] = model
        
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
        
gettag = GetTag()