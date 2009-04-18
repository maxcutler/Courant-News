from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from courant.core.news.sitemaps import news_sitemaps
from courant.core.media.sitemaps import media_sitemaps
from courant.core.events.sitemaps import events_sitemaps
from courant.core.pages.sitemaps import pages_sitemaps
sitemaps = {}
sitemaps.update(news_sitemaps)
sitemaps.update(media_sitemaps)
sitemaps.update(events_sitemaps)
sitemaps.update(pages_sitemaps)

from courant.core.siteconfig.forms import SettingsForm
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^courant2/', include('courant2.foo.urls')),
    (r'^admin/settings/$',
        'courant.core.siteconfig.views.site_settings',
        {'form_class': SettingsForm}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/obj_lookup/$', 'courant.core.genericadmin.views.generic_lookup'),
    (r'^admin/(.*)', admin.site.root),

    (r'^%s(?P<path>.*)$' % settings.COURANT_ADMIN_MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.COURANT_ADMIN_MEDIA_ROOT}),
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    (r'^sitemap.xml$',
        'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    (r'^emailthis/', include('courant.core.emailthis.urls')),

    (r'^contact/', include('courant.core.contact_form.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^events/', include('courant.core.events.urls')),

    (r'^staff/', include('courant.core.staff.urls')),

    (r'^media/', include('courant.core.media.urls')),

    (r'^search', include('courant.core.search.urls')),

    (r'^accounts/', include('courant.core.registration.urls')),
    (r'^profiles/', include('courant.core.profiles.urls')),

    (r'^mostpopular/', include('courant.core.countthis.urls')),

    (r'^', include('courant.core.news.urls')),
    (r'^', include('courant.core.pages.urls')),
)
