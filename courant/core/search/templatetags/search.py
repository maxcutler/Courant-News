from django.template import Library, Node, Variable
from courant.core.search.forms import CourantSearchForm

register = Library()

class SearchFacetCheck(Node):
    def __init__(self, facet, value, varname):
        self.facet = facet
        self.value = value
        self.varname = varname
        
    def render(self, context):
        request = context['request']
        facets = request.GET.getlist('selected_facets')
        found = False
        facet_type = unicode(Variable(self.facet).resolve(context))
        value = unicode(Variable(self.value).resolve(context))
        for facet in facets:
            if len(facet) > 0:
                name, id = facet.split(':')
                if name == facet_type and id == value:
                    found = True
                    break
            context[self.varname] = found
        return ''
    
def do_search_facet_check(parser, token):
    bits = token.contents.split()
    if not len(bits) == 5:
        raise TemplateSyntaxError, "search_facet_check syntax error"
    return SearchFacetCheck(bits[1], bits[2], bits[4])
do_search_facet_check = register.tag('search_facet_check', do_search_facet_check)

def strip_facet(url, facet, value):
    to_remove = "&selected_facets=%s:%s" % (facet, value)
    return url.replace('%3A', ':').replace(to_remove, '')
register.simple_tag(strip_facet)

class SearchFormNode(Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        context[self.varname] = CourantSearchForm(context['request'].GET)
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


class SearchObject(Node):
    def __init__(self, obj, varname):
        self.obj = obj
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = Variable(self.obj).resolve(context)._object
        return ''
    
def get_search_object(parser, token):
    """
    Extracts a model instance object from a search query result object
    """
    bits = token.contents.split()
    if not len(bits) == 4:
        raise TemplateSyntaxError, "get_search_object syntax invalid"
    return SearchObject(bits[1], bits[3])
get_search_object = register.tag(get_search_object)