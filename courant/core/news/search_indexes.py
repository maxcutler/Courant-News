from haystack import indexes
from haystack import site
from models import Article
from django.contrib.contenttypes.models import ContentType

class ArticleIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='heading')
    section = indexes.IntegerField(model_attr='section__pk')
    published_at = indexes.DateTimeField(model_attr='published_at')
    type = indexes.IntegerField()
    staffers = indexes.MultiValueField()
    
    def prepare_type(self, object):
        return ContentType.objects.get_for_model(Article).pk
      
    def prepare_staffers(self, object):
        return [s.id for s in object.authors.all()]
        
    def get_queryset(self):
        return Article.live.all()
    
    def get_updated_field(self):
        return 'modified_at'
    
site.register(Article, ArticleIndex)