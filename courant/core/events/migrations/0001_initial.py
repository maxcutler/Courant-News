
from south.db import db
from django.db import models
from courant.core.events.models import *

class Migration:
    
    def forwards(self):
        
        # Model 'EventType'
        db.create_table('events_eventtype', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=100)),
            ('slug', models.SlugField()),
        ))
        
        # Mock Models
        EventType = db.mock_model(model_name='EventType', db_table='events_eventtype', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Event'
        db.create_table('events_event', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=255)),
            ('slug', models.SlugField()),
            ('summary', models.TextField()),
            ('description', models.TextField()),
            ('event_type', models.ForeignKey(EventType)),
            ('tags', TagField()),
            ('date', models.DateField()),
            ('start_time', models.TimeField()),
            ('end_time', models.TimeField(blank=True, null=True)),
            ('verified', models.BooleanField()),
            ('submitted_by', models.ForeignKey(User, blank=True, null=True)),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
        ))
        
        db.send_create_signal('events', ['EventType','Event'])
    
    def backwards(self):
        db.delete_table('events_event')
        db.delete_table('events_eventtype')
        
