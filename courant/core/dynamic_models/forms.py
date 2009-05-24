from django import forms
from django.contrib.contenttypes.models import ContentType

from courant.core.dynamic_models.models import *

class DynamicTypeAdminForm(forms.ModelForm):
    @property
    def eligible_bases(self):
        choices = []
        for subclass in DynamicModelBase.__subclasses__():
            ct = ContentType.objects.get_for_model(subclass)
            choices.append((ct.id, unicode(ct))) 
        print choices
        return choices

    def __init__(self, *args, **kwargs):
        super(DynamicTypeAdminForm, self).__init__(*args, **kwargs)
        self.fields['base'].choices = self.eligible_bases
        
    class Meta:
        model = DynamicType
    
    