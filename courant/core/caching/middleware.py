from django.core.cache import cache
from django import http
import re
import settings


class MemcachedMiddleware:
    # based on http://soyrex.com/blog/django-nginx-and-memcached/

    def process_response(self, request, response):
        try:
          if not isinstance(response, http.HttpResponsePermanentRedirect):
            cacheIt = True
            theUrl = request.get_full_path()

            # if it's a GET then store it in the cache:
            if request.method != 'GET' or not request.user.is_anonymous():
                cacheIt = False

            # loop on our CACHE_INGORE_REGEXPS and ignore
            # certain urls.
            for exp in settings.CACHE_IGNORE_REGEXPS:
                if re.match(exp, theUrl):
                    cacheIt = False

            if cacheIt:
                key = '%s-%s' % (settings.CACHE_KEY_PREFIX, theUrl)
                cache.set(key, response.content, 3600)

            # delete any sessionid remnants for non-authenticated users
            # django leaves an invalid sessionid cookie after logout, which
            # screws up our caching
            if not request.user.is_authenticated() and \
                'sessionid' in request.COOKIES and \
                len(request.COOKIES['sessionid']):

                response.delete_cookie('sessionid')
        except:
          pass
        return response
