from haystack import indexes
from haystack import site
from models import *
from django.contrib.contenttypes.models import ContentType

class MediaItemIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, model_attr='caption')
    title = indexes.CharField(model_attr='name')
    published_at = indexes.DateTimeField(model_attr='published_at')
    type = indexes.IntegerField()
    staffers = indexes.MultiValueField()
    
    def prepare_type(self, object):
        return ContentType.objects.get_for_model(object.as_leaf_class()).pk
      
    def prepare_staffers(self, object):
        return [s.id for s in object.staffers.all()]
        
    def get_updated_field(self):
        return 'modified_at'
    
site.register(Photo, MediaItemIndex)
site.register(Video, MediaItemIndex)
site.register(Audio, MediaItemIndex)
site.register(Gallery, MediaItemIndex)