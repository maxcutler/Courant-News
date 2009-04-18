from django.conf.urls.defaults import *

from courant.core.pages.views import *

urlpatterns = patterns('',
    url(r'(?P<url>.*)/$', render_page, name="page"),
)