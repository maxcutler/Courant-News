from django.template import TemplateDoesNotExist
from django.conf import settings

from courant.core.pages.models import Page
from courant.core.pages.views import render_page

class TemplatePagesMiddleware(object):
    #Heavily adapted from the Django flatpage middleware - http://code.djangoproject.com/browser/django/trunk/django/contrib/flatpages/middleware.py

    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.

        # Try and render the page
        try:
            url = request.path_info if request.path_info[-1] != '/' else request.path_info[1:-1]
            return render_page(request, url)
        # If the page doesn't exist, return the response
        except (Page.DoesNotExist, TemplateDoesNotExist):
            return response
        # If it's another error and we're in DEBUG, raise the error, or just return the response
        except:
            if settings.DEBUG:
                raise
            return response