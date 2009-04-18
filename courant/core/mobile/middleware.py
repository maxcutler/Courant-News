from django.conf import settings
import re


class MobileMiddleware(object):

    def process_request(self, request):
        domain = request.META.get('HTTP_HOST', '').split('.')

        if 'm' in domain or 'mobile' in domain or \
            (settings.MOBILE_DEBUG == 'mobile' or settings.MOBILE_DEBUG == 'iphone'):

            #Check iPhone UA
            ua = re.compile('iPhone|iPod', re.IGNORECASE)
            if ua.search(request.META['HTTP_USER_AGENT']) or settings.MOBILE_DEBUG == 'iphone':
                request.extension = 'iphone'
            else:
                request.extension = 'mobile'
