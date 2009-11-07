
from south.db import db
from django.db import models
from courant.core.caching.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'CachedObject'
        db.create_table('caching_cachedobject', (
            ('id', models.AutoField(primary_key=True)),
            ('cache_key', models.CharField(max_length=255)),
            ('url', models.CharField(max_length=255)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'])),
            ('object_id', models.PositiveIntegerField()),
            ('modified_at', ModificationDateTimeField()),
        ))
        db.send_create_signal('caching', ['CachedObject'])
        db.create_index('caching_cachedobject', ['content_type_id', 'object_id'])
        db.create_index('caching_cachedobject', ['url', 'content_type_id', 'object_id', 'cache_key'])
        db.create_index('caching_cachedobject', ['modified_at'])



    def backwards(self, orm):
        # Deleting model indices
        db.delete_index('caching_cachedobject', ['modified_at'])
        db.delete_index('caching_cachedobject', ['url', 'content_type_id', 'object_id', 'cache_key'])
        db.delete_index('caching_cachedobject', ['content_type_id', 'object_id'])

        # Deleting model 'CachedObject'
        db.delete_table('caching_cachedobject')



    models = {
        'caching.cachedobject': {
            'cache_key': ('models.CharField', [], {'max_length': '255'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('ModificationDateTimeField', [], {}),
            'object_id': ('models.PositiveIntegerField', [], {}),
            'url': ('models.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['caching']
