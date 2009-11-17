from django.contrib import admin

from courant.core.staff.models import *


class StafferAdmin(admin.ModelAdmin):

    list_display = ['last_name', 'first_name', 'user', 'public_profile']
    list_filter = ['public_profile']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'first_name', 'last_name']
admin.site.register(Staffer, StafferAdmin)

admin.site.register(StaffPositionTitle)
admin.site.register(StaffDepartment)
admin.site.register(StaffPosition)