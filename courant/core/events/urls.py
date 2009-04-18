from django.conf.urls.defaults import *
from courant.core.events.views import *

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', event_detailed, name="event_detailed"),

    url(r'^today/$', event_archive, {'year': datetime.datetime.now().year,
                                     'month': datetime.datetime.now().month,
                                     'day': datetime.datetime.now().day}, name="event_archive_today"),

    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/(?P<day>\w{1,2})/$', event_archive, name="event_archive_day"),
    url(r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', event_archive, name="event_archive_month"),
    url(r'^(?P<year>\d{4})/$', event_archive, name="event_archive_year"),
    url(r'^$', event_archive, name="event_archive"),
    url(r'^submit/$', event_submit, name="event_submit"),
)
