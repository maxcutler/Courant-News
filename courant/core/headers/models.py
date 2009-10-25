from django.db import models

class HttpHeader(models.Model):
    """
    HTTP headers and descriptions. Populated with initial ones from a migration.
    """
    
    name = models.CharField(max_length=50)
    header = models.CharField(max_length=50)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name

class HeaderRule(models.Model):
    """
    A rule that changes the file extension and/or sets a context variable based on an HTTP header.
    """
    
    name = models.CharField(max_length=50)
    header = models.ForeignKey(HttpHeader)
    regex = models.CharField(max_length=255)
    
    domain = models.CharField(max_length=50, blank=True)
    extension_list = models.CharField(max_length=50, default="html")
    context_var = models.CharField(max_length=50, blank=True)
    
    order = models.PositiveSmallIntegerField()
    
    enabled = models.BooleanField('Enable This Rule')
    admin_override = models.BooleanField('Enable This Rule for Admins for Testing')
    
    def __unicode__(self):
        return self.name