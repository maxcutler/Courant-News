from django.db import models
from django.db.models.query import QuerySet

# Following queryset, manager, and models are based on the snippet at
# http://www.djangosnippets.org/snippets/1034/
class SubclassQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    def __iter__(self):
        for item in super(SubclassQuerySet, self).__iter__():
            yield item.as_leaf_class()

class SubclassManager(models.Manager):
    def get_query_set(self):
        return SubclassQuerySet(self.model)