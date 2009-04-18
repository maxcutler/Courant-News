from django.template import Library, Node
from courant.core.search.forms import SearchForm

register = Library()

class SearchFormNode(Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        context[self.varname] = SearchForm(context['request'].GET)
        return ''

def get_search_form(parser, token):
    """
    Sets a search form to a variable. Form is as follows:
    get_search_form as varname
    """
    bits = token.contents.split()
    if not len(bits) == 3:
        raise TemplateSyntaxError, "get_search_form only takes 'as varname'"
    return SearchFormNode(bits[2])
get_search_form = register.tag(get_search_form)