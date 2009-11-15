from django.contrib import admin

from courant.core.nando.workflow.models import *

class WorkflowAdmin(admin.ModelAdmin):
    pass
admin.site.register(Workflow, WorkflowAdmin)

class WorkflowStatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(WorkflowStatus, WorkflowStatusAdmin)