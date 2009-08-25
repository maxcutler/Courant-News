from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.fields import DateField, TimeField

from courant.core.utils.forms.widgets import SplitSelectDateTimeWidget, SelectTimeWidget
from courant.core.gettag import gettag
from courant.core.search import search
from courant.core.dynamic_models.models import DynamicModelBase

from tagging.fields import TagField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from djangosphinx.manager import SphinxSearch

import datetime


class EventType(models.Model):
    """
    A type or category of events.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name
gettag.register(EventType)

class Event(DynamicModelBase):
    """
    A scheduled event.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    summary = models.TextField()
    description = models.TextField()

    event_type = models.ForeignKey(EventType, related_name="events")
    tags = TagField()
    #location when we make the location app

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)

    verified = models.BooleanField(help_text="Approved by staff to appear on site.")
    submitted_by = models.ForeignKey(User, blank=True, null=True)

    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()

    search = SphinxSearch('events')

    class Meta:
        ordering = ['-date', 'start_time']
        get_latest_by = 'date'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return('event_detailed', (), {
            'slug': self.slug,
            'year': self.date.year,
            'month': "%02d" % self.date.month,
            'day': "%02d" % self.date.day,
        })

    def start_datetime(self):
        """
        Create Python datetime for the starting time of the event.
        """
        return datetime.datetime.combine(self.date, self.start_time)
gettag.register(Event)
search.register(Event,
                fields=('name', 'summary'),
                filter_fields=('event_type','verified','event_type','submitted_by'),
                date_field='date')

class EventForm(ModelForm):
    date = DateField(widget=SplitSelectDateTimeWidget(twelve_hr=True))
    end_time = TimeField(widget=SelectTimeWidget(twelve_hr=True))

    class Meta:
        exclude = ('slug', 'start_time', 'submitted_by', 'verified')
        model = Event
