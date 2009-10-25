from courant.core.headers.models import HeaderRule
from django.db.models import Q
import re

class HttpHeadersMiddleware(object):

    def process_request(self, request):
        HEADER_VARS = {}
        extensions_done = False
        rules = HeaderRule.objects.all().filter(Q(enabled=True) | Q(admin_override=True))
        
        for rule in rules:
        
            """
            This if statement only looks complex because it's multiline
            Basically, if the user is an admin and the admin override is enabled then it works
            Otherwise, it checks if the rule is enabled, the domain matches, and the header regex matches
            """

            if (rule.admin_override and request.user.is_superuser) \
            or ( \
            rule.enabled and \
            re.match(rule.domain, request.META.get('HTTP_HOST')) and \
            re.search(rule.regex, request.META.get("HTTP_" + rule.header.header.replace('-', '_').upper())) \
            ):
                
                #Only set extensions for first rule that matches
                if not extensions_done:
                    #Add extensions to request.extension, stripping any leading dots
                    request.extension = [ext.lstrip('.') for ext in rule.extension_list.split(' ')]
                    extensions_done = True
                        
                #Set context variable if it exists
                if rule.context_var:
                    HEADER_VARS[rule.context_var] = True
                
        #Attach any context vars to the request object
        request.HEADER_VARS = HEADER_VARS