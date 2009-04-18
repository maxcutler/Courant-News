from south.db import db
from django.db import models
from courant.core.discussions.models import *


class Migration:

    def forwards(self, orm):
        # Adding model 'CommentOptions'
        db.create_table('discussions_commentoptions', (
            ('name', models.CharField(max_length=50)),
            ('moderate_after', models.PositiveSmallIntegerField(default=30)),
            ('allow_anonymous', models.BooleanField()),
            ('moderate_anonymous_only', models.BooleanField()),
            ('close_after', models.PositiveSmallIntegerField(default=365)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('discussions', ['CommentOptions'])

        # Adding model 'DefaultCommentOption'
        db.create_table('discussions_defaultcommentoption', (
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], unique=True)),
            ('options', models.ForeignKey(orm.CommentOptions)),
        ))
        db.send_create_signal('discussions', ['DefaultCommentOption'])

    def backwards(self, orm):
        # Deleting model 'CommentOptions'
        db.delete_table('discussions_commentoptions')

        # Deleting model 'DefaultCommentOption'
        db.delete_table('discussions_defaultcommentoption')

    models = {
        'discussions.commentoptions': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
        }
    }
