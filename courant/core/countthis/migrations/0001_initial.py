
from south.db import db
from django.db import models
from courant.core.countthis.models import *


class Migration:

    def forwards(self, orm):

        # Adding model 'Statistic'
        db.create_table('countthis_statistic', (
            ('view_count', models.PositiveIntegerField(default=0)),
            ('email_count', models.PositiveIntegerField(default=0)),
            ('created_at', CreationDateTimeField()),
            ('object_id', models.PositiveIntegerField()),
            ('comment_count', models.PositiveIntegerField(default=0)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'])),
            ('path', models.CharField(max_length=255)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('countthis', ['Statistic'])

    def backwards(self, orm):

        # Deleting model 'Statistic'
        db.delete_table('countthis_statistic')

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)",
                     'unique_together': "(('app_label','model'),)",
                     'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
        }
    }
