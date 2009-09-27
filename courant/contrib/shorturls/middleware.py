from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponsePermanentRedirect
from django.conf import settings
from django.db.models import F
from models import Shorturl, ShorturlHit

class ShortUrlMiddleware(object):
    """
    Handles redirecting users to the appropriate URL.  If a response object with
    an HTTP 404 status makes it to this middleware, it will check for any short
    URLs whose shortcuts match the requested path.  If a match is found,
    the hit count for the Itty Bitty URL is incremented and the user is
    redirected to the corresponding URL.  If no matching short URL is found
    the HTTP 404 will continue to bubble up.
    """
    def process_response(self, request, response):
        if response.status_code in [404, 500] and request.path.startswith(settings.SHORTURLS_PREFIX):
            try:
                path = request.path[len(settings.SHORTURLS_PREFIX):].strip('/')
                url = get_object_or_404(Shorturl, url__exact=path)
                hits = ShorturlHit.objects.get_or_create(medium=url.medium,
                                                         shorturl=url)
                ShorturlHit.objects.filter(medium=url.medium, shorturl=url).update(count=F('count')+1)
                return HttpResponsePermanentRedirect(url.content_object.get_absolute_url())
            except Http404:
                return response
            except:
                if settings.DEBUG:
                    raise

        return response