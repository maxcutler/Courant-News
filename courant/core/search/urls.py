from django.conf.urls.defaults import *
from courant.core.search.views import *

urlpatterns = patterns('',
    url(r'', search, name="search"),
)
