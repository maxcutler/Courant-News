from django.template import Library, Node, Variable
from django.template.loader import get_template
from courant.core.search.didyoumean import get_didyoumean

#register = Library()

class DidYouMeanNode(Node):
    def __init__(self, terms, min, count):
        self.terms = terms
        self.min = int(min)
        self.count = count
   
    def render(self, context):
        self.terms = Variable(self.terms).resolve(context)
        self.count = int(Variable(self.count).resolve(context))
        
        #We have enough results
        if self.min < self.count:
            return ''
        else:
            context['newterms'] = get_didyoumean(self.terms)
            
            if not context['newterms']:
                return ''
            
            #Render template
            t = get_template('search/didyoumean.html')
            return t.render(context)

"""
Usage is "didyoumean terms [min count]"
Min and count must be set or not set together. If set, didyoumean will only show if count is greater than min.
"""
def didyoumean(parser, token):
    bits = token.contents.split()
    if not len(bits) == 2 and not len(bits) == 4:
        raise TemplateSyntaxError
    else:
        if len(bits) == 4:
            min = bits[2]
            count = bits[3]
        else:
            min = None
            count = None
    return DidYouMeanNode(bits[1], min, count)
#didyoumean = register.tag(didyoumean)