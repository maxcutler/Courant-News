from django.contrib import admin
from django import forms
from courant.core.sharethis.models import *


class SocialNetworkForm(forms.ModelForm):

    class Meta:
        model = SocialNetwork

    def clean_name(self):
        data = self.cleaned_data['name']
        if data.lower() == 'all':
            raise forms.ValidationError('You may not name your Social Network "all". Please choose a different name.')
        return data


class SocialNetworkAdmin(admin.ModelAdmin):
    form = SocialNetworkForm

    list_display = ['name', 'enabled']
    list_filter = ['enabled']
    search_fields = ['name']
    ordering = ['name']

admin.site.register(SocialNetwork, SocialNetworkAdmin)
