from django import forms

from models import Section

class ArticleAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields['section'].choices = sections_as_choices()

def sections_as_choices():
    sections = []
    for section in Section.objects.filter(parent=None):
        sub_sections = []
        for sub_section in Section.objects.filter(full_path__startswith=section.full_path):
            if section.pk != sub_section.pk:
                sub_sections.append([sub_section.id, sub_section.name])
        
        # if the section has children, add this section as a header
        if len(sub_sections) > 0:
            sections.append([section.name, sub_sections])
        else:
            # otherwise just add the section as a selectable choice
            sections.append((section.id, section))
    
    return sections