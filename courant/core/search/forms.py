from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime
from haystack.forms import FacetedSearchForm
from courant.core.news.models import Article

class CourantSearchForm(FacetedSearchForm):
    start_date = forms.DateField(required=False, widget=SelectDateWidget(years=range(Article.objects.order_by('published_at')[0].published_at.year,datetime.date.today().year+1)))
    end_date = forms.DateField(required=False, widget=SelectDateWidget(years=range(Article.objects.order_by('published_at')[0].published_at.year,datetime.date.today().year+1)))
    
    def __init__(self, *args, **kwargs):
        super(CourantSearchForm, self).__init__(*args, **kwargs)
        oldest_article_date = Article.objects.order_by('published_at')[0].published_at
        self.fields['start_date'].widget = SelectDateWidget(years=range(oldest_article_date.year,datetime.date.today().year+1))
        self.fields['end_date'].widget = SelectDateWidget(years=range(oldest_article_date.year,datetime.date.today().year+1))
    
    def search(self):
        sqs = super(CourantSearchForm, self).search()
        
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(published_at__gte=self.cleaned_data['start_date'])
        
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(published_at__lte=self.cleaned_data['end_date'])
            
        return sqs