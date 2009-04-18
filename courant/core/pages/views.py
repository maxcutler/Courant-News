from django.template import TemplateDoesNotExist

from courant.core.pages.models import Page
from courant.core.utils import render

def render_page(request, url):
    page = Page.objects.get(url=url)
    #[:-5] is to strip the HTML
    return render(request, ['pages'+page.template[:-5],])