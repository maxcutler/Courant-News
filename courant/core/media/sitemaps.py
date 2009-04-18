from django.contrib.sitemaps import Sitemap

from courant.core.media.models import MediaItem

from datetime import date, timedelta

class MediaSitemap(Sitemap):
    priority = 0.5
    limit = 10000 # if each sitemap file has too many articles, it takes too long to generate

    def items(self):
        return MediaItem.objects.all()
        
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
        
media_sitemaps = {
    'media': MediaSitemap,
}
    