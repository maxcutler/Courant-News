
from south.db import db
from django.db import models
from courant.core.maps.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Map'
        db.create_table('maps_map', (
            ('mediaitem_ptr', models.OneToOneField(orm['media.MediaItem'])),
            ('provider', models.ForeignKey(orm.Provider, null=True, blank=True)),
            ('center_longitude', models.DecimalField(null=True, max_digits=11, decimal_places=8, blank=True)),
            ('center_latitude', models.DecimalField(null=True, max_digits=11, decimal_places=8, blank=True)),
            ('zoom', models.PositiveSmallIntegerField(null=True, blank=True)),
            ('map_type', models.CharField(blank=True, max_length=10, null=True)),
        ))
        db.send_create_signal('maps', ['Map'])
        
        # Adding model 'Provider'
        db.create_table('maps_provider', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('template', models.CharField(max_length=255)),
        ))
        db.send_create_signal('maps', ['Provider'])
        
        # Adding model 'Location'
        db.create_table('maps_location', (
            ('id', models.AutoField(primary_key=True)),
            ('dynamic_type', models.ForeignKey(orm['dynamic_models.DynamicType'], default=None, null=True, blank=True)),
            ('name', models.CharField(max_length=255)),
            ('slug', models.SlugField(unique=True)),
            ('parent', models.ForeignKey(orm.Location, related_name='sublocations', null=True, blank=True)),
            ('address', models.CharField(max_length=255, blank=True)),
            ('description', models.TextField()),
            ('longitude', models.DecimalField(max_digits=11, decimal_places=8, blank=True)),
            ('latitude', models.DecimalField(max_digits=11, decimal_places=8, blank=True)),
        ))
        db.send_create_signal('maps', ['Location'])
        
        # Adding ManyToManyField 'Map.locations'
        db.create_table('maps_map_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('map', models.ForeignKey(orm.Map, null=False)),
            ('location', models.ForeignKey(orm.Location, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Map'
        db.delete_table('maps_map')
        
        # Deleting model 'Provider'
        db.delete_table('maps_provider')
        
        # Deleting model 'Location'
        db.delete_table('maps_location')
        
        # Dropping ManyToManyField 'Map.locations'
        db.delete_table('maps_map_locations')
        
    
    
    models = {
        'media.mediaitem': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'dynamic_models.dynamictype': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media.mediafolder': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'maps.map': {
            'Meta': {'_bases': ['courant.core.media.models.MediaItem']},
            'center_latitude': ('models.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'center_longitude': ('models.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'locations': ('models.ManyToManyField', ["orm['maps.Location']"], {'related_name': "'maps'", 'blank': 'True'}),
            'map_type': ('models.CharField', [], {'blank': 'True', 'max_length': '10', 'null': 'True'}),
            'mediaitem_ptr': ('models.OneToOneField', ["orm['media.MediaItem']"], {}),
            'provider': ('models.ForeignKey', ["orm['maps.Provider']"], {'null': 'True', 'blank': 'True'}),
            'zoom': ('models.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'maps.location': {
            'address': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('models.TextField', [], {}),
            'dynamic_type': ('models.ForeignKey', ["orm['dynamic_models.DynamicType']"], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('models.DecimalField', [], {'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'longitude': ('models.DecimalField', [], {'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'parent': ('models.ForeignKey', ["orm['maps.Location']"], {'related_name': "'sublocations'", 'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'discussions.commentoptions': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'maps.provider': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'template': ('models.CharField', [], {'max_length': '255'})
        },
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['maps']
