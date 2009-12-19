from django.contrib import admin

from courant.core.maps.models import *

class MapAdmin(admin.ModelAdmin):
    pass
admin.site.register(Map, MapAdmin)

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)

class ProviderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Provider, ProviderAdmin)