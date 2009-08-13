from django.template import Library, Template, TemplateSyntaxError, Node, Variable
from courant.contrib.shorturls.models import ShorturlMedium, Shorturl

register = Library()

class ShorturlNode(Node):
    def __init__(self, obj, medium, varname=None):
        self.obj = Variable(obj)
        self.medium = medium
        self.varname = varname
        
    def render(self, context):
        obj = self.obj.resolve(context)
        
        medium, created = ShorturlMedium.objects.get_or_create(name__iexact=self.medium,
                                                               defaults={'name':self.medium})
        
        shorturl, created = Shorturl.objects.get_or_create(medium=medium,
                                                           content_type=obj.content_type,
                                                           object_id=obj.pk)
        
        if self.varname:
            context[self.varname] = shorturl.get_shortcut()
            return ''
        else:
            return shorturl.get_shortcut()
        
def do_shorturl(parser, token):
    """
    Retrives the shorturl for a content object for a given publication medium.
    
    Syntax::
    
        {% shorturl obj medium %}
        {% shorturl obj medium as varname %}
    
    Examples::
    
        {% shorturl article twitter %}
        {% shorturl event email %}
        {% shorturl photo print as photo_url %}
    """
    bits = token.contents.split()
    if len(bits) != 3 and len(bits) != 5:
        raise template.TemplateSyntaxError("Invalid arguments to 'shorturl' template tag")
    if (len(bits) == 5):
        return ShorturlNode(bits[1], bits[2], bits[4])
    else:
        return ShorturlNode(bits[1], bits[2])
register.tag('shorturl', do_shorturl)