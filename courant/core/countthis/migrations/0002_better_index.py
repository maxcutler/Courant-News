
from south.db import db
from django.db import models
from courant.core.countthis.models import *

class Migration:
    
    def forwards(self, orm):
        db.create_index('countthis_statistic', ['content_type_id', 'created_at'])
    
    
    def backwards(self, orm):
        db.delete_index('countthis_statistic', ['content_type_id', 'created_at'])
    
    
    models = {
        'countthis.statistic': {
            'Meta': {'unique_together': "['content_type','object_id']"},
            'comment_count': ('models.PositiveIntegerField', [], {'default': '0'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {}),
            'created_at': ('CreationDateTimeField', [], {}),
            'email_count': ('models.PositiveIntegerField', [], {'default': '0'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.PositiveIntegerField', [], {}),
            'path': ('models.CharField', [], {'max_length': '255'}),
            'view_count': ('models.PositiveIntegerField', [], {'default': '0'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['countthis']
