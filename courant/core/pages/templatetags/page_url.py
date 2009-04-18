from django import template
from django.template import TemplateSyntaxError

from courant.core.pages.models import Page

register = template.Library()

@register.simple_tag
def page_url(slug):
    try:
        return Page.objects.get(slug=slug).get_absolute_url()
    except:
        return ''
        #raise TemplateSyntaxError, "No page found with slug: " + slug