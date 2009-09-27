from django.db import models
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

from utils import gen_shortcut

import random

class ShorturlMedium(models.Model):
    """
    Specific publishing medium in which the short URL link will appear
    
    For example, Twitter, email, print, etc.
    """
    name = models.CharField(max_length="255")
    random_code = models.PositiveIntegerField(unique=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self, **kwargs):
        if not self.pk:
            while True:
                self.random_code = random.randint(0, 100)
                if ShorturlMedium.objects.filter(random_code=self.random_code).count() == 0:
                    break
        super(ShorturlMedium, self).save(**kwargs)
    
class Shorturl(models.Model):
    """
    A per-medium short URL for a content object.
    """
    medium = models.ForeignKey(ShorturlMedium)
    url = models.CharField(max_length=255, blank=True, unique=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        ordering = ('-created_at', 'url')
    
    def __unicode__(self):
        return unicode(self.content_object)
        
    def save(self, **kwargs):
        if not self.pk or not self.url:
            if settings.SHORTURLS_VARIETY:
                num = 0
                
                # loop until we find a new unique URL
                while True:
                    # only perform the calculation on the first loop iteration
                    if num == 0:
                        # create varied URL by interleaving the three unique components
                        a = unicode(self.content_type.pk)
                        b = unicode(self.object_id)
                        c = unicode(self.medium.random_code)
                        max_width = max(len(a), len(b), len(c))

                        # pad out components for optimal interleaving
                        components = [a.center(max_width, '_'),
                                      b.center(max_width, '_'),
                                      c.center(max_width, '_')]
        
                        # interleave unique components
                        interleaved = [ y for x in map(None,a,b,c) for y in x if y and y != '_']
                        num = int(''.join(interleaved))
                    else:
                        num += 1 # increment until we find a valid value

                    self.url = gen_shortcut(num)

                    if Shorturl.objects.filter(url=self.url).count() == 0:
                        break
            else:
                self.url = gen_shortcut(Shorturl.objects.count()+1)
        super(Shorturl, self).save(**kwargs)
 
    def get_shortcut(self):
        return ''.join([settings.SHORTURLS_DOMAIN or (Site.objects.get_current().domain+settings.SHORTURLS_PREFIX),
                        self.url])
        
class ShorturlHit(models.Model):
    """
    Tracks hits for each short URL (per-medium).
    """
    medium = models.ForeignKey(ShorturlMedium)
    shorturl = models.ForeignKey(Shorturl)
    count = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return "%s: %d" % (self.shorturl, self.count)