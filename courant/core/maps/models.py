from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.exceptions import ValidationError

from courant.core.media.models import MediaItem
from courant.core.gettag import gettag
from courant.core.dynamic_models.models import DynamicModelBase

import os

MAP_TYPE_CHOICES = (
    ('ROAD', 'Road'),
    ('SATELLITE', 'Satellite'),
    ('HYBRID', 'Hybrid'),
)

class Provider(models.Model):
    name = models.CharField(max_length=255)
    template = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
class Map(MediaItem):
    """
    Media item representing a map.
    """
    
    provider = models.ForeignKey(Provider, blank=True, null=True)
    center_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    center_latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    zoom = models.PositiveSmallIntegerField(null=True, blank=True)
    map_type = models.CharField(max_length=10, choices=MAP_TYPE_CHOICES, null=True, blank=True)
    
    locations = models.ManyToManyField('Location', related_name='maps', blank=True)
        
    def __unicode__(self):
        return u"Map: %s" % self.name
        
    def thumbnail(self):
        return "map_thumbnail.gif"

gettag.register(Map)

class Location(DynamicModelBase):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name='sublocations')
    
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, )
    latitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_coordinates(self):
        if self.latitude is not None and self.longitude is not None:
            return {"latitude": self.latitude, "longitude": self.longitude}
        elif self.parent:
            return self.parent.get_coordinates()
        else:
            return None

def geocode(params):
    from django.utils.http import urlencode
    from urllib import urlopen

    params = urlencode(params)
    geocode = urlopen("http://maps.google.com/maps/geo?%s" % params).read()
    
    split = geocode.split(',')
    
    if split[2] == '0':
        return False
    else:
        return {
            "latitude": split[2],
            "longitude": split[3]
        }

#Hook into presave signal to geocode the address
def pre_save_geocode(sender, instance, **kwargs):
    #If lat/long aren't set yet, geocode
    if not instance.latitude or not instance.longitude or instance.address != Location.objects.filter(id=instance.id).values_list('address', flat=True)[0]:

        params = [
            ('q', instance.address),
            ("output", "csv")
        ]
        
        latlong = geocode(params)
        
        if latlong:
            instance.latitude = latlong['latitude']
            instance.longitude = latlong['longitude']
        else:
            if instance.get_coordinates():
                coords = instance.get_coordinates()
                instance.latitude = coords['latitude']
                instance.longitude = coords['longitude']
            else:
                raise ValidationError, "The address could not be geocoded and no parent with a valid latitude and longitude was found."
pre_save.connect(pre_save_geocode, sender=Location)