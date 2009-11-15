
from south.db import db
from django.db import models
from courant.core.media.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'MediaItem.workflow_status'
        db.add_column('media_mediaitem', 'workflow_status', models.ForeignKey(orm['workflow.WorkflowStatus'], null=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'MediaItem.workflow_status'
        db.delete_column('media_mediaitem', 'workflow_status_id')
        
    
    
    models = {
        'media.mediaitem': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"'},
            'caption': ('models.TextField', [], {}),
            'comment_options': ('models.ForeignKey', ["orm['discussions.CommentOptions']"], {'null': 'True'}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': "{'app_label':'media'}", 'null': 'True', 'editable': 'False'}),
            'created_at': ('CreationDateTimeField', [], {}),
            'folder': ('models.ForeignKey', ["orm['media.MediaFolder']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('ModificationDateTimeField', [], {}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'published_at': ('models.DateTimeField', [], {}),
            'slug': ('models.SlugField', [], {}),
            'staffers': ('models.ManyToManyField', ["orm['staff.Staffer']"], {'related_name': "'media'", 'through': "'MediaByline'"}),
            'staffers_override': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status_line_override': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'workflow_status': ('models.ForeignKey', ["orm['workflow.WorkflowStatus']"], {'null': 'True'})
        },
        'media.file': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"', '_bases': ['courant.core.media.models.MediaItem']},
            'file': ('models.FileField', ["_('file')"], {}),
            'height': ('models.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('models.ImageField', ['"Thumbnail"'], {'blank': 'True'}),
            'mediaitem_ptr': ('models.OneToOneField', ["orm['media.MediaItem']"], {}),
            'width': ('models.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'media.video': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"', '_bases': ['courant.core.media.models.MediaItem']},
            'image': ('models.ImageField', ['"Thumbnail"'], {'blank': 'True'}),
            'mediaitem_ptr': ('models.OneToOneField', ["orm['media.MediaItem']"], {}),
            'url': ('models.URLField', [], {})
        },
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media.photo': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"', '_bases': ['courant.core.media.models.MediaItem']},
            'image': ('models.ImageField', ["_('image')"], {}),
            'mediaitem_ptr': ('models.OneToOneField', ["orm['media.MediaItem']"], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media.gallery': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"', '_bases': ['courant.core.media.models.MediaItem']},
            'media': ('models.ManyToManyField', ["orm['media.MediaItem']"], {'related_name': "'galleries'", 'through': "'GalleryMedia'", 'symmetrical': 'False'}),
            'mediaitem_ptr': ('models.OneToOneField', ["orm['media.MediaItem']"], {})
        },
        'media.audio': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"', '_bases': ['courant.core.media.models.MediaItem']},
            'file': ('models.FileField', [], {}),
            'mediaitem_ptr': ('models.OneToOneField', ["orm['media.MediaItem']"], {})
        },
        'workflow.workflowstatus': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media.mediabyline': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_item': ('models.ForeignKey', ["orm['media.MediaItem']"], {}),
            'order': ('models.PositiveSmallIntegerField', [], {}),
            'position': ('models.CharField', [], {'max_length': '100'}),
            'staffer': ('models.ForeignKey', ["orm['staff.Staffer']"], {})
        },
        'discussions.commentoptions': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media.mediafolder': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'level': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lft': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'parent': ('models.ForeignKey', ["orm['media.MediaFolder']"], {'related_name': "'children'", 'null': 'True', 'blank': 'True'}),
            'rght': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tree_id': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'media.gallerymedia': {
            'gallery': ('models.ForeignKey', ["orm['media.Gallery']"], {'related_name': "'gallery_media'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_item': ('models.ForeignKey', ["orm['media.MediaItem']"], {}),
            'order': ('models.PositiveSmallIntegerField', [], {})
        }
    }
    
    complete_apps = ['media']
