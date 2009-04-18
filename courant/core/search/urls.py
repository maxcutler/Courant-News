from django.conf.urls.defaults import *
from courant.core.views import *

urlpatterns = patterns('',
    url(r'', search, name="search"),
)
