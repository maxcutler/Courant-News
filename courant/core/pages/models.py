from django.db import models
from django.conf import settings
import os

class Page(models.Model):
    """
    A static or custom page on the website.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    url = models.CharField(max_length=255)
    template = models.FilePathField(max_length=255, path=os.path.join(settings.SITE_TEMPLATE_DIR,'pages',), match=".*\.html$", recursive=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return('page', (), {
            'url': self.url
        })