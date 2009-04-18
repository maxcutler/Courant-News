from django.conf.urls.defaults import *
from courant.core.media.views import *

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', media_detailed,name="media_detailed"),
)