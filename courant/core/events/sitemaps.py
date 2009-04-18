from django.contrib.sitemaps import Sitemap
from courant.core.events.models import Event

from datetime import date, timedelta

class EventsSitemap(Sitemap):
    priority = 0.2
    changefreq = 'yearly'
    limit = 15000 # if each sitemap file has too many articles, it takes too long to generate

    def items(self):
        return Event.objects.filter(verified=True)

    def lastmod(self, obj):
        return obj.modified_at
        
events_sitemaps = {
    'events': EventsSitemap,
}
    