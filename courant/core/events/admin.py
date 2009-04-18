from django.contrib import admin
from django import forms

from courant.core.events.models import *


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['name', 'event_type', 'date', 'start_time', 'verified']
    list_filter = ['event_type', 'verified']
    search_fields = ['name', 'summary']

    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Event, EventAdmin)


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

    prepopulated_fields = {'slug': ('name',)}
admin.site.register(EventType, EventTypeAdmin)
