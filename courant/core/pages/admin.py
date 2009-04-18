from django.contrib import admin
from django.forms import ModelForm

from courant.core.pages.models import *
from courant.core.pages.forms import RelativeFilePathField

class PageAdminForm(ModelForm):
    template = RelativeFilePathField(path=os.path.join(settings.SITE_TEMPLATE_DIR,'pages',), match=".*\.html$", recursive=True)
    
    class Meta:
        model = Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = PageAdminForm
admin.site.register(Page, PageAdmin)