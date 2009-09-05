from django.contrib import admin
from django.contrib.contenttypes import generic
from courant.core.dynamic_models.models import *
from courant.core.dynamic_models.forms import *

class DynamicTypeFieldAdmin(admin.StackedInline):
    model = DynamicTypeField
    extra = 2

class DynamicTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'base']
    list_filter = ['base']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    form = DynamicTypeAdminForm
    
    inlines = [DynamicTypeFieldAdmin]
admin.site.register(DynamicType, DynamicTypeAdmin)

class AttributeInline(generic.GenericTabularInline):
    model = Attribute
    extra = 0