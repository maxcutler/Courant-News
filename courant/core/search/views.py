from courant.core.search.forms import SearchForm
from courant.core.utils import render

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

class CourantSearchView(FacetedSearchView):
    
    def get_results(self):
        r = super(CourantSearchView, self).get_results()
        if isinstance(r, SearchQuerySet):
            return r.load_all()
        return r
    
    def build_page(self):
        return (None, self.results)

#import copy
#def search(request):
#    results = {}
#    params = request.GET.copy() #Since request.GET is immutable, we need to create a copy to manipulate
#    
#    params.setlistdefault('indexes', ['articles',]) #Make sure at least articles is checked
#    indexes = copy.deepcopy(params.getlist('indexes')) #deepcopy so articles_delta isn't injected into params, messing up the form
#    if 'articles' in indexes:
#        indexes.append('articles_delta')
#    indexes = str(' '.join(indexes)) #Sphinx wants a string, not a unicode
#    
#    form = SearchForm(params)
#    
#    if request.GET['q']:
#        if form.is_valid():
#            results = SphinxQuerySet(index=indexes).query(form.cleaned_data['q']).set_options(mode=SPH_MATCH_EXTENDED)
#            if form.cleaned_data['end_date']:
#                results = results.filter(date__lte=form.cleaned_data['end_date'])
#            if form.cleaned_data['start_date']:
#                results = results.filter(date__gte=form.cleaned_data['start_date'])
#            if form.cleaned_data['sort_by'] == 'date':
#                results = results.order_by('-date')
#    return render(request, ['search/results_page'], {'form': form, 'results':results, 'terms':request.GET['q'] })