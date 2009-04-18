from django import template
from django.contrib.comments.models import Comment

register = template.Library()

@register.inclusion_tag('comments/moderation_links.html', takes_context=True)
def moderation_links(context, comment):
    return {'comment':comment, 'context':context}
    
class PendingListNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
      
    def render(self, context):
        context[self.varname] = Comment.objects.filter(is_public=False, is_removed=False).order_by('content_type', 'object_pk')
        return ''

def do_pending_list(parser, token):
    """
    {% pending_list as list %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "pending_list: Invalid template tag parameters."
    return PendingListNode(bits[2])
register.tag('pending_list', do_pending_list)