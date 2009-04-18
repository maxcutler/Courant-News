class AlreadyRegistered(Exception):
    """
    An attempt was made to register a model for get tag more than once.
    """
    pass

class SearchRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self,
                 model,
                 fields=None,
                 filter_fields=None,
                 date_field='published_at',
                 use_delta=False):
        """
        Sets the given model class up for working with tags.
        """
        if model in self._registry:
            raise AlreadyRegistered(
                _('The model %s has already been registered.') % model.__name__)
        
        self._registry[model] = {'fields': fields,
                                 'filter_fields': filter_fields,
                                 'date_field': date_field,
                                 'use_delta': use_delta}
        
    def unregister(self, model):
        if model in self._registry:
            del self._registry[model]       
search = SearchRegistry()