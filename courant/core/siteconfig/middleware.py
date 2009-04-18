#Adapted from http://code.google.com/p/reviewboard/source/browse/trunk/reviewboard/admin/middleware.py
# and http://svn.navi.cx/misc/trunk/djblets/djblets/siteconfig/middleware.py

from courant.core.siteconfig.siteconfig import load_site_config
from courant.core.siteconfig.models import SiteConfiguration

class LoadSettingsMiddleware:
    """
    Middleware that loads the settings on each request.
    """

    def process_request(self, request):
        # Load all site settings.
        load_site_config()
        return None


class ExpireSettingsMiddleware(object):
    """
    Middleware that performs necessary operations for siteconfig settings.

    Right now, the primary responsibility is to check on each request if
    the settings have expired, so that a web server worker process doesn't
    end up with a stale view of the site settings.
    """

    def process_request(self, request):
        SiteConfiguration.objects.check_expired()
        return None
