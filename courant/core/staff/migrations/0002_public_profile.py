
from south.db import db
from django.db import models
from courant.core.staff.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Staffer.public_profile'
        db.add_column('staff_staffer', 'public_profile', models.BooleanField(default=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Staffer.public_profile'
        db.delete_column('staff_staffer', 'public_profile')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
            'first_name': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'position': ('models.CharField', [], {'max_length': '255'}),
            'public_profile': ('models.BooleanField', [], {'default': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['staff']
