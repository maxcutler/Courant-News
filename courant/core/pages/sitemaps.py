from django.contrib.sitemaps import Sitemap
from django.conf import settings

from courant.core.pages.models import Page

from datetime import date, timedelta, datetime

import os

class PagesSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    limit = 10000 # if each sitemap file has too many articles, it takes too long to generate

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        path = os.path.normpath(os.path.sep.join([settings.SITE_TEMPLATE_DIR,'pages',obj.template]))
        return datetime.fromtimestamp(os.path.getmtime(path))

pages_sitemaps = {
    'pages': PagesSitemap,
}
    