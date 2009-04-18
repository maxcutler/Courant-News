from django.conf.urls.defaults import *
from courant.core.staff.views import *

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', staffer_detailed, name="staffer_detailed"),
)
