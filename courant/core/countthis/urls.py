from django.conf.urls.defaults import *
from courant.core.countthis.views import *

urlpatterns = patterns('',
    url(r'^(?P<type>[A-Za-z]+)/(?P<days>\d+)/$', most_popular, name="most_popular"),
    url(r'^(?P<type>[A-Za-z]+)/$', most_popular, name="most_popular"),
    url(r'^(?P<days>\d+)/$', most_popular, name="most_popular"),
    url(r'^$', most_popular, name="most_popular"),
)
