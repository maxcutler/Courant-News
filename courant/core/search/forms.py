from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

class SearchForm(forms.Form):
    q = forms.CharField(min_length=2, max_length=100, label='Search Terms', required=False)
    start_date = forms.DateField(required=False, )#widget=SelectDateWidget(years=range(1996,datetime.date.today().year+1)))
    end_date = forms.DateField(required=False, )#widget=SelectDateWidget(years=range(1996,datetime.date.today().year+1)))
    sort_by = forms.ChoiceField(choices=(
                                        ('relevance', 'Relevance',),
                                        ('date', 'Date',)
                                        ,),
                                required=False,
                               )
    indexes = forms.MultipleChoiceField(choices=(
                                        ('articles', 'Articles',),
                                        ('events', 'Events',)
                                        ,),
                                label="What To Search",
                                widget=forms.CheckboxSelectMultiple,
                                required=False,
                               )