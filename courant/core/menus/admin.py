from django.contrib import admin
from django import forms
from django.conf import settings

from courant.core.menus.models import *

class MenuLocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(MenuLocation, MenuLocationAdmin)

class MenuItemInline(admin.TabularInline):
    fields = ('order', 'name', 'content_type', 'object_id', 'url',)
    model = MenuItem

class MenuAdmin(admin.ModelAdmin):
    list_display = ['name','location','active_url','active']
    list_filter = ['location']
    
    inlines = [
        MenuItemInline,
    ]
admin.site.register(Menu, MenuAdmin)
