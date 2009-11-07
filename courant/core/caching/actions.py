from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from courant.core.caching.models import clear_obj_cache

def clear_admin_obj_cache(modeladmin, request, queryset):
	for obj in queryset:
		clear_obj_cache(obj)
clear_admin_obj_cache.short_description = 'Clear cache for object'
admin.site.add_action(clear_admin_obj_cache)