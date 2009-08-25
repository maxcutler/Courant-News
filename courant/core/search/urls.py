from django.conf.urls.defaults import *
from courant.core.search.views import *

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

urlpatterns = patterns('',
    url(r'', CourantSearchView(template='search/results_page.html',
                               form_class=FacetedSearchForm,
                               searchqueryset=SearchQuerySet().facet('section')), name="search"),
)
