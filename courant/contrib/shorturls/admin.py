from django.contrib import admin

from models import *

class ShorturlAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'url', 'medium']
    list_filter = ['medium', 'content_type']
admin.site.register(Shorturl, ShorturlAdmin)
admin.site.register(ShorturlMedium)

class ShorturlHitAdmin(admin.ModelAdmin):
    list_display = ['medium', 'shorturl', 'count']
    list_filter = ['medium']
admin.site.register(ShorturlHit, ShorturlHitAdmin)