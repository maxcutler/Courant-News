
from south.db import db
from django.db import models
from courant.core.maps.models import *

class Migration:
    
    def forwards(self, orm):
        
        orm.Provider(name="Microsoft", template="microsoft").save()
        orm.Provider(name="Google V3", template="googlev3").save()
        orm.Provider(name="Google", template="google").save()
        orm.Provider(name="Yahoo", template="yahoo").save()

    def backwards(self, orm):
        
        pass
        
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
