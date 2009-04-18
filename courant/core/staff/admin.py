from django.contrib import admin

from courant.core.staff.models import *


class StafferAdmin(admin.ModelAdmin):

    list_display = ['user', 'position']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(Staffer, StafferAdmin)
