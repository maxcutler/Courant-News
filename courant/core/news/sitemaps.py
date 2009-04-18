from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from datetime import date, timedelta

from courant.core.news.models import Article, Issue, Section

class ArticleSitemap(Sitemap):
    priority = 0.5
    limit = 10000 # if each sitemap file has too many articles, it takes too long to generate

    def items(self):
        return Article.objects.all()
        
    def changefreq(self, obj):
        delta = date.today() - obj.published_at.date()
        if delta.days > 30:
            return 'monthly'
        elif delta.days > 7:
            return 'weekly'
        else:
            return 'daily'

    def lastmod(self, obj):
        return obj.published_at

class IssueSitemap(Sitemap):
    priority = 0.5
    
    def items(self):
        return Issue.objects.all()
        
    def changefreq(self, obj):
        delta = date.today() - obj.published_at.date()
        if delta.days > 30:
            return 'yearly'
        else:
            return 'daily'
        
    def lastmod(self, obj):
        return obj.published_at
    
class SectionSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    
    def items(self):
        return Section.objects.all()
        
    def lastmod(self, obj):
        a = Article.objects.filter(section__full_path__startswith=obj.full_path)
        if a.count() > 0:
            return a[0].published_at
        else:
            return None
        
class HomepageSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'
    
    def items(self):
        return ['homepage']
    
    def location(self, obj):
        return reverse('homepage')
        
news_sitemaps = {
    'articles':ArticleSitemap,
    'issues': IssueSitemap,
    'sections': SectionSitemap,
    'homepage': HomepageSitemap,
}
    