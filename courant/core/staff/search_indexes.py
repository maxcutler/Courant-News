from haystack import indexes
from haystack import site
from models import Staffer
from django.contrib.contenttypes.models import ContentType

class StafferIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True)
    title = indexes.CharField()
    type = indexes.IntegerField()
    
    def prepare_text(self, object):
        return ('%s %s ' % (object.first_name, object.last_name)) * 10
        
    def prepare_title(self, object):
        return unicode(object)
    
    def prepare_type(self, object):
        return ContentType.objects.get_for_model(Staffer).pk
        
    def get_queryset(self):
        return Staffer.objects.filter(public_profile=True)
    
site.register(Staffer, StafferIndex)