from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

def obj_for_page(qs, path):
    def compareUrlDepth(objA, objB):
        return objB.active_url().count('/') - objA.active_url().count('/')
        
    objs = list(qs)
    objs.sort(cmp=compareUrlDepth)
    
    # match the path
    for obj in objs:
        if path.startswith(obj.active_url()):
            return obj
    return None

class MenuLocation(models.Model):
    """
    A position on a page or somewhere in the website where a menu will be rendered.
    """
    name = models.CharField(max_length=100)
    
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    
    def __unicode__(self):
        return self.name
    
    def menu_for_page(self, path):
        """
        Determines which menu to render in this location based on the current
        URL path.
        """
        try:
            return Menu.objects.get(location=self, active=True)
        except (Menu.DoesNotExist, Menu.MultipleObjectsReturned):
            return obj_for_page(Menu.objects.filter(location=self), path)

class Menu(models.Model):
    """
    A collection of MenuItems that can be rendered in a given MenuLocation
    based on a certain criteria and the page being rendered.
    """
    name = models.CharField(max_length=100)
    location = models.ForeignKey(MenuLocation, related_name='menus')
    active = models.BooleanField('Always Use For Location')
    
    url = models.CharField(max_length=100, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    
    def __unicode__(self):
        return self.name
    
    def active_url(self):
        """
        Determines the base URL for which this menu should be rendered.
        """
        if self.url:
            return self.url
        elif self.content_object and hasattr(self.content_object,'get_absolute_url'):
            return self.content_object.get_absolute_url()
        else:
            return ''
        
    def item_for_page(self, path):
        """
        Determines the active menu item in this menu for the given path.
        """
        return obj_for_page(MenuItem.objects.filter(menu=self), path)

class MenuItem(models.Model):
    """
    A single link in a menu. Can link either to a specific content object or
    an arbitrary URL.
    """
    name = models.CharField('Link Text', max_length=100)
    menu = models.ForeignKey(Menu, related_name='menuitems')
    
    url = models.CharField(max_length=100, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    order = models.PositiveSmallIntegerField()

    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()
    
    class Meta:
        ordering = ('order',)
    
    def __unicode__(self):
        if self.url:
            return self.url
        else:
            return unicode(self.content_object)
        
    def active_url(self):
        """
        Determines the base URL for which this menu item should be rendered.
        """
        if self.url:
            return self.url
        elif self.content_object and hasattr(self.content_object,'get_absolute_url'):
            return self.content_object.get_absolute_url()
        else:
            return ''