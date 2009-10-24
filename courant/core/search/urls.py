from django.conf.urls.defaults import *

import datetime

from haystack.query import SearchQuerySet

from courant.core.search.views import CourantSearchView
from courant.core.search.forms import CourantSearchForm

urlpatterns = patterns('',
    url(r'', CourantSearchView(template='search/results_page.html',
                               form_class=CourantSearchForm,
                               searchqueryset=SearchQuerySet().facet('section').facet('staffers').facet('type')), name="search"),
)
