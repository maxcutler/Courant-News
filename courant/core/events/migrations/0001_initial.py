
from south.db import db
from django.db import models
from courant.core.events.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', models.AutoField(primary_key=True)),
            ('dynamic_type', models.ForeignKey(orm['dynamic_models.DynamicType'], null=True)),
            ('name', models.CharField(max_length=255)),
            ('slug', models.SlugField()),
            ('summary', models.TextField()),
            ('description', models.TextField()),
            ('event_type', models.ForeignKey(orm.EventType, related_name="events")),
            ('tags', TagField()),
            ('date', models.DateField()),
            ('start_time', models.TimeField()),
            ('end_time', models.TimeField(null=True, blank=True)),
            ('verified', models.BooleanField()),
            ('submitted_by', models.ForeignKey(orm['auth.User'], null=True, blank=True)),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
        ))
        db.send_create_signal('events', ['Event'])
        
        # Adding model 'EventType'
        db.create_table('events_eventtype', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=100)),
            ('slug', models.SlugField()),
        ))
        db.send_create_signal('events', ['EventType'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('events_event')
        
        # Deleting model 'EventType'
        db.delete_table('events_eventtype')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'events.event': {
            'Meta': {'ordering': "['-date','start_time']", 'get_latest_by': "'date'"},
            'created_at': ('CreationDateTimeField', [], {}),
            'date': ('models.DateField', [], {}),
            'description': ('models.TextField', [], {}),
            'dynamic_type': ('models.ForeignKey', ["orm['dynamic_models.DynamicType']"], {'null': 'True'}),
            'end_time': ('models.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('models.ForeignKey', ["orm['events.EventType']"], {'related_name': '"events"'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('ModificationDateTimeField', [], {}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'slug': ('models.SlugField', [], {}),
            'start_time': ('models.TimeField', [], {}),
            'submitted_by': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'summary': ('models.TextField', [], {}),
            'tags': ('TagField', [], {}),
            'verified': ('models.BooleanField', [], {})
        },
        'dynamic_models.dynamictype': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'events.eventtype': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'slug': ('models.SlugField', [], {})
        }
    }
    
    complete_apps = ['events']
