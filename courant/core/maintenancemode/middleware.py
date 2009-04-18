from django.core import urlresolvers
from django.conf import settings
from django.conf.urls import defaults
defaults.handler503 = 'maintenancemode.views.defaults.temporary_unavailable'
defaults.__all__.append('handler503')

class MaintenanceModeMiddleware(object):
    def process_request(self, request):
        from courant.core.maintenancemode.conf.settings import MAINTENANCE_MODE
        
        # Allow access if middleware is not activated
        if not MAINTENANCE_MODE:
            return None
        
        if request.path[0:7] == '/admin/':
            #Let admin access through always
            return None

        # Allow access if remote ip is in INTERNAL_IPS
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return None
        
        # Allow acess if the user doing the request is logged in and a
        # staff member.
        if hasattr(request, 'user') and request.user.is_staff:
            return None
        
        # Otherwise show the user the 503 page
        resolver = urlresolvers.get_resolver(None)
        
        callback, param_dict = resolver._resolve_special('503')
        return callback(request, **param_dict)