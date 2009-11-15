from django.contrib import admin

from courant.core.nando.lifecycle.models import *

class PitchAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pitch, PitchAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Assignment, AssignmentAdmin)