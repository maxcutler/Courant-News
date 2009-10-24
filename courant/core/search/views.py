from courant.core.search.forms import CourantSearchForm
from courant.core.utils import render

from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

class CourantSearchView(FacetedSearchView):
    def __call__(self, request):
        self.request = request
        
        self.date_sort = (request.GET.get('order', '') == 'date')
        
        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()
        
        return self.create_response()
        
    def get_results(self):
        if self.query:
            if self.date_sort:
                return self.form.search().order_by('-published_at')
            return self.form.search()
        
        return []
    
    def extra_context(self):
        extra = {}
        
        if self.query:
            facets = self.form.search().facet_counts()
            
            for field, values in facets['fields'].items():
                # sort in descending order
                values.sort(lambda x,y:cmp(y[1],x[1]))
                
                # remove any null values or empty facets
                # e.g., media don't have sections, so section facets show up as null
                to_remove = []
                for index, value in enumerate(values):
                    if value[0] == None or value[1] == 0:
                        # must delete from end of list towards front, or else indexes will change
                        to_remove.insert(0, index) 
                for index in to_remove:
                    del values[index]
    
            extra['facets'] = facets
            extra['results'] = self.results
            extra['sort_order'] = 'date' if self.date_sort else 'relevance'
        return extra