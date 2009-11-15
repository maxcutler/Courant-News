
from south.db import db
from django.db import models
from courant.core.media.models import *

class Migration:

    depends_on = (
	    ("discussions", "0002_initial"),
    )
    
    def forwards(self, orm):
        
        # Adding model 'MediaItem'
        db.create_table('media_mediaitem', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('caption', models.TextField()),
            ('folder', models.ForeignKey(orm.MediaFolder)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={'app_label':'media'}, null=True, editable=False)),
            ('staffers_override', models.CharField(max_length=255, blank=True)),
            ('status_line_override', models.CharField(max_length=255, blank=True)),
            ('slug', models.SlugField()),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
            ('published_at', models.DateTimeField()),
            ('tags', TagField()),
            ('comment_options', models.ForeignKey(orm['discussions.CommentOptions'], default=None, null=True)),
        ))
        db.send_create_signal('media', ['MediaItem'])
        
        # Adding model 'File'
        db.create_table('media_file', (
            ('mediaitem_ptr', models.OneToOneField(orm['media.MediaItem'])),
            ('file', models.FileField(_('file'))),
            ('image', models.ImageField("Thumbnail", blank=True)),
            ('width', models.PositiveIntegerField(null=True, blank=True)),
            ('height', models.PositiveIntegerField(null=True, blank=True)),
        ))
        db.send_create_signal('media', ['File'])
        
        # Adding model 'Video'
        db.create_table('media_video', (
            ('mediaitem_ptr', models.OneToOneField(orm['media.MediaItem'])),
            ('url', models.URLField()),
            ('image', models.ImageField("Thumbnail", blank=True)),
        ))
        db.send_create_signal('media', ['Video'])
        
        # Adding model 'Photo'
        db.create_table('media_photo', (
            ('mediaitem_ptr', models.OneToOneField(orm['media.MediaItem'])),
            ('image', models.ImageField(_('image'))),
        ))
        db.send_create_signal('media', ['Photo'])
        
        # Adding model 'Gallery'
        db.create_table('media_gallery', (
            ('mediaitem_ptr', models.OneToOneField(orm['media.MediaItem'])),
        ))
        db.send_create_signal('media', ['Gallery'])
        
        # Adding model 'Audio'
        db.create_table('media_audio', (
            ('mediaitem_ptr', models.OneToOneField(orm['media.MediaItem'])),
            ('file', models.FileField()),
        ))
        db.send_create_signal('media', ['Audio'])
        
        # Adding model 'MediaByline'
        db.create_table('media_mediabyline', (
            ('id', models.AutoField(primary_key=True)),
            ('staffer', models.ForeignKey(orm['staff.Staffer'])),
            ('position', models.CharField(max_length=100)),
            ('order', models.PositiveSmallIntegerField()),
            ('media_item', models.ForeignKey(orm.MediaItem)),
        ))
        db.send_create_signal('media', ['MediaByline'])
        
        # Adding model 'MediaFolder'
        db.create_table('media_mediafolder', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('parent', models.ForeignKey(orm.MediaFolder, related_name='children', null=True, blank=True)),
            ('lft', models.IntegerField()),
            ('rght', models.IntegerField()),
            ('tree_id', models.IntegerField()),
            ('level', models.IntegerField()),
        ))
        db.send_create_signal('media', ['MediaFolder'])
        
        # Adding model 'GalleryMedia'
        db.create_table('media_gallerymedia', (
            ('id', models.AutoField(primary_key=True)),
            ('media_item', models.ForeignKey(orm.MediaItem)),
            ('order', models.PositiveSmallIntegerField()),
            ('gallery', models.ForeignKey(orm.Gallery, related_name='gallery_media')),
        ))
        db.send_create_signal('media', ['GalleryMedia'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'MediaItem'
        db.delete_table('media_mediaitem')
        
        # Deleting model 'File'
        db.delete_table('media_file')
        
        # Deleting model 'Video'
        db.delete_table('media_video')
        
        # Deleting model 'Photo'
        db.delete_table('media_photo')
        
        # Deleting model 'Gallery'
        db.delete_table('media_gallery')
        
        # Deleting model 'Audio'
        db.delete_table('media_audio')
        
        # Deleting model 'MediaByline'
        db.delete_table('media_mediabyline')
        
        # Deleting model 'MediaFolder'
        db.delete_table('media_mediafolder')
        
        # Deleting model 'GalleryMedia'
        db.delete_table('media_gallerymedia')
        
    
    
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
            'tags': ('TagField', [], {})
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
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
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
            'level': ('models.IntegerField', [], {}),
            'lft': ('models.IntegerField', [], {}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'parent': ('models.ForeignKey', ["orm['media.MediaFolder']"], {'related_name': "'children'", 'null': 'True', 'blank': 'True'}),
            'rght': ('models.IntegerField', [], {}),
            'tree_id': ('models.IntegerField', [], {})
        },
        'media.gallerymedia': {
            'gallery': ('models.ForeignKey', ["orm['media.Gallery']"], {'related_name': "'gallery_media'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_item': ('models.ForeignKey', ["orm['media.MediaItem']"], {}),
            'order': ('models.PositiveSmallIntegerField', [], {})
        }
    }
    
    complete_apps = ['media']
