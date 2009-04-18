
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
            ('name', models.CharField(max_length=255)),
            ('tags', TagField()),
            ('staffers_override', models.CharField(max_length=255, blank=True)),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
            ('slug', models.SlugField()),
            ('caption', models.TextField()),
            ('published_at', models.DateTimeField()),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={'app_label':'media'}, null=True, editable=False)),
            ('folder', models.ForeignKey(orm.MediaFolder)),
            ('comment_options', models.ForeignKey(orm['discussions.CommentOptions'], null=True, default=None)),
            ('id', models.AutoField(primary_key=True)),
            ('status_line_override', models.CharField(max_length=255, blank=True)),
        ))
        db.send_create_signal('media', ['MediaItem'])
        
        # Adding model 'Video'
        db.create_table('media_video', (
            ('url', models.URLField()),
            ('image', models.ImageField("Thumbnail", upload_to=get_storage_path, blank=True)),
            ('mediaitem_ptr', models.OneToOneField(orm.MediaItem)),
        ))
        db.send_create_signal('media', ['Video'])
        
        # Adding model 'Photo'
        db.create_table('media_photo', (
            ('image', models.ImageField(('image'), upload_to=get_storage_path)),
            ('mediaitem_ptr', models.OneToOneField(orm.MediaItem)),
        ))
        db.send_create_signal('media', ['Photo'])
        
        # Adding model 'Gallery'
        db.create_table('media_gallery', (
            ('mediaitem_ptr', models.OneToOneField(orm.MediaItem)),
        ))
        db.send_create_signal('media', ['Gallery'])
        
        # Adding model 'Audio'
        db.create_table('media_audio', (
            ('file', models.FileField(upload_to=get_file_path)),
            ('mediaitem_ptr', models.OneToOneField(orm.MediaItem)),
        ))
        db.send_create_signal('media', ['Audio'])
        
        # Adding model 'MediaByline'
        db.create_table('media_mediabyline', (
            ('media_item', models.ForeignKey(orm.MediaItem)),
            ('position', models.CharField(max_length=100)),
            ('staffer', models.ForeignKey(orm['staff.Staffer'])),
            ('id', models.AutoField(primary_key=True)),
            ('order', models.PositiveSmallIntegerField()),
        ))
        db.send_create_signal('media', ['MediaByline'])
        
        # Adding model 'MediaFolder'
        db.create_table('media_mediafolder', (
            ('rght', models.IntegerField()),
            ('name', models.CharField(max_length=255)),
            ('parent', models.ForeignKey(orm.MediaFolder, related_name='children', null=True, blank=True)),
            ('level', models.IntegerField()),
            ('lft', models.IntegerField()),
            ('tree_id', models.IntegerField()),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('media', ['MediaFolder'])
        
        # Adding model 'GalleryMedia'
        db.create_table('media_gallerymedia', (
            ('gallery', models.ForeignKey(orm.Gallery, related_name='gallery_media')),
            ('media_item', models.ForeignKey(orm.MediaItem)),
            ('id', models.AutoField(primary_key=True)),
            ('order', models.PositiveSmallIntegerField()),
        ))
        db.send_create_signal('media', ['GalleryMedia'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'MediaItem'
        db.delete_table('media_mediaitem')
        
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
        
        # Dropping ManyToManyField 'Gallery.media'
        db.delete_table('media_gallerymedia')
        
        # Dropping ManyToManyField 'MediaItem.staffers'
        db.delete_table('media_mediabyline')
        
    
    
    models = {
        'media.mediaitem': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media.gallery': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"', '_bases': ['courant.core.media.models.MediaItem']},
            '_stub': True,
            'mediaitem_ptr': ('models.OneToOneField', ['MediaItem'], {})
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
        'media.mediafolder': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    
