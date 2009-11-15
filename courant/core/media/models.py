from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache

from courant.core.staff.models import Staffer, ContentByline
from courant.core.discussions.models import CommentOptions, DefaultCommentOption
from courant.core.utils.managers import SubclassManager
from courant.core.gettag import gettag
from courant.core.nando.workflow.models import WorkflowMixin

import tagging
from tagging.fields import TagField

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from courant.core.media.utils import get_file_path, get_storage_path, get_image_path

from sorl.thumbnail.main import DjangoThumbnail
from sorl.thumbnail.base import ThumbnailException

import mptt
from datetime import datetime
import urllib
import os

class MediaFolder(models.Model):
    """
    A folder in a virtual tree-like file system that can be used to organize the
    library of media content. 
    """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return "%s/%s" % ('/'.join(self.get_ancestors().values_list('name', flat=True)), self.name)

    def indented_name(self):
        """
        Only for use in the admin change list to show the tree heirarchy.
        """
        indents = self.level
        return '-- ' * indents + self.name
    indented_name.short_description = 'Name'
mptt.register(MediaFolder, order_insertion_by=['name'])

class MediaItem(WorkflowMixin):
    """
    Abstract base class for all types of media content. Allows placement in
    library folder system, association with staffers, and other basic fields that
    all media content should share (e.g., slug, tags, comments).
    
    Not strictly a Django abstract model to allow for manipulation in the admin
    interface and in scripts. However, one should never create a new MediaItem
    instance directly.
    
    When querying on MediaItem manager, all results will be casted to their
    actual content type class (e.g., Photo). This allows for querying of all
    media without needing to merge the results of queries against each media
    type individually. 
    """
    name = models.CharField(max_length=255,
                            help_text="Short description to be used as a \
                                      headline or link text.")
    caption = models.TextField()
    folder = models.ForeignKey(MediaFolder)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'app_label': 'media'},
                                     editable=False, null=True)
    
    staffers = models.ManyToManyField(Staffer, through='MediaByline', related_name='media')
    staffers_override = models.CharField(max_length=255, blank=True,
                                         help_text="Override normal staffer \
                                                   associations, esp. for one-off \
                                                   contributors.")
    status_line_override = models.CharField(max_length=255, blank=True,
                                            help_text="Override normal staffer \
                                                      associations, esp. for one-off \
                                                      contributors.")
    
    slug = models.SlugField()
    
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    published_at = models.DateTimeField()
    
    tags = TagField()
    
    def default_comment_option():
        try:
            defaults = cache.get('default_mediaitem_comment_options')
            if not defaults:
                defaults = DefaultCommentOption.objects.get(content_type=ContentType.objects.get_for_model(MediaItem)).options
                cache.set('default_mediaitem_comment_options', defaults)
            return defaults
        except:
            return None

    comment_options = models.ForeignKey(CommentOptions, null=True, default=default_comment_option)
    
    objects = SubclassManager()
    
    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
    
    def __unicode__(self):
        return "Media: %s" % self.name
    
    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return('media_detailed', (), {
            'slug': self.slug,
            'year': self.published_at.year,
            'month': "%02d" % self.published_at.month,
            'day': "%02d" % self.published_at.day,
        })

    def as_leaf_class(self):
        """
        Casts to actual content type.
        """
        content_type = self.content_type
        model = content_type.model_class()
        if (model == MediaItem):
            return self
        return model.objects.get(id=self.id)
        
    def admin_thumbnail(self):
        """
        Returns an image for display in admin listings.
        """
        if hasattr(self, 'thumbnail'):
            try:
                thumb = DjangoThumbnail(self.thumbnail(), (160,120), opts={'crop':True})
                return '<img src="%s" width="160" height="120" />' % unicode(thumb)
            except ThumbnailException:
                return 'N/A'
        return 'N/A'
    admin_thumbnail.allow_tags = True
    admin_thumbnail.short_description = 'Thumbnail'
gettag.register(MediaItem, plural_name='media')

class MediaByline(ContentByline):
    """
    Associates a staffer with a media item, including their position and the
    order to display this staffer among all staffers associated with the item.
    """
    media_item = models.ForeignKey(MediaItem)
    
class ContentMedia(models.Model):
    """
    Abstract base class for associating media with a content object, including
    specifying an order in which all such associations should be displayed.
    """
    media_item = models.ForeignKey(MediaItem)
    order = models.PositiveSmallIntegerField()
    
    class Meta:
        abstract = True
        ordering = ['order']
    
class Photo(MediaItem):
    """
    Media item representing a photo or other image.
    """
    image = models.ImageField(_('image'), upload_to=get_storage_path)
    
    objects = SubclassManager()
    
    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        
    def __unicode__(self):
        return u"Photo: %s" % self.name
    
    def thumbnail(self):
        return self.image
gettag.register(Photo)

class Video(MediaItem):
    """
    Media item representing a video from an external video service that
    supports the OEmbed protocol.
    
    Currently only support YouTube videos.
    """
    url = models.URLField(help_text="Full URL of the video, in format:<br>http://www.youtube.com/v/id-here")
    image = models.ImageField("Thumbnail", upload_to=get_storage_path, blank=True,
                              help_text="Leave blank to automatically fetch from external service.")
    
    objects = SubclassManager()
    
    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        
    def __unicode__(self):
        return u"Video: %s" % self.name
    
    def save(self, **kwargs):
        if not self.image:
            youtube_id = self.url.split('/')[-1]
            filename = get_image_path(self, "%s_thumb.jpg" % youtube_id)
            sys_path = os.path.join(settings.MEDIA_ROOT,filename.replace('/',os.sep))
            if not os.path.exists(sys_path):
                try:
                    os.makedirs(os.path.join(settings.MEDIA_ROOT, filename[:filename.rindex('/')].replace('/', os.sep)))
                except os.error:
                    pass
                file = urllib.urlretrieve("http://img.youtube.com/vi/%s/0.jpg" % youtube_id,sys_path)
            self.image = filename
        super(Video, self).save(**kwargs)
        
    def thumbnail(self):
        return self.image
gettag.register(Video)

class Audio(MediaItem):
    """
    Media item representing an audio file.
    """
    file = models.FileField(upload_to=get_file_path)
    
    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        
    def __unicode__(self):
        return u"Audio: %s" % self.name
gettag.register(Audio)
  
class Gallery(MediaItem):
    """
    Media item representing a collection of other media items. Typically to be
    rendered in a gallery or slideshow format.
    """
    media = models.ManyToManyField(MediaItem, through='GalleryMedia',
                                   related_name='galleries', symmetrical=False)
    
    objects = SubclassManager()
    
    def __init__(self, *args, **kwargs):
        super(Gallery, self).__init__(*args, **kwargs)
        
        # fetch the first item in the gallery to be used for thumbnail purposes
        try:
            setattr(self, 'image', self.gallery_media.order_by('order')[0].media_item.as_leaf_class().image)
        except:
            pass
    
    class Meta:
        verbose_name_plural = 'galleries'
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        
    def __unicode__(self):
        return u"Gallery: %s" % self.name
    
    def thumbnail(self):
        return self.image
gettag.register(Gallery)    

class GalleryMedia(ContentMedia):
    """
    Associates media items to galleries in a specified order.
    """
    gallery = models.ForeignKey(Gallery, related_name='gallery_media')
    
class File(MediaItem):
    """
    Media item representing a file.
    """
    file = models.FileField(_('file'), upload_to=get_file_path)
    image = models.ImageField("Thumbnail", upload_to=get_storage_path, blank=True,
                              help_text="Leave blank to generate automatically.")
    
    width = models.PositiveIntegerField(blank=True, null=True, help_text="Only required for certain file types (e.g., SWF)")
    height = models.PositiveIntegerField(blank=True, null=True, help_text="Only required for certain file types (e.g., SWF)")
    
    objects = SubclassManager()
    
    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        
    def thumbnail(self):
        return self.image if self.image else self.file
    
    def extension(self):
        """
        Returns file extension without leading dot (e.g., 'pdf', 'swf')
        """
        basename, extension = os.path.splitext(self.file.name)
        return extension[1:]
gettag.register(File)