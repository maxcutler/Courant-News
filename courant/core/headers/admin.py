from django.contrib import admin

from courant.core.headers.models import *

class HeaderRuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(HeaderRule, HeaderRuleAdmin)

class HttpHeaderAdmin(admin.ModelAdmin):
    pass
admin.site.register(HttpHeader, HttpHeaderAdmin)