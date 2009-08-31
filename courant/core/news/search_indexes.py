from haystack import indexes
from haystack import site
from models import Article

class ArticleIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='heading')
    section = indexes.CharField(model_attr='section__name')
    published_at = indexes.DateTimeField(model_attr='published_at')
    
    #rendered = indexes.CharField(use_template=True, indexed=False)
    
    def get_queryset(self):
        return Article.live.all()
    
    def get_updated_field(self):
        return 'modified_at'
    
site.register(Article, ArticleIndex)