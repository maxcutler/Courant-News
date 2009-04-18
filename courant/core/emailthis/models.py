import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import django.dispatch

email_sent = django.dispatch.Signal(providing_args=["instance"])

class EmailEvent(models.Model):
    content_type=models.ForeignKey(ContentType)
    object_id=models.IntegerField()
    content_object=generic.GenericForeignKey()
    
    mailed_by=models.ForeignKey(User, null=True, blank=True)
    email_from=models.EmailField("Your Email", help_text="required")
    email_to=models.CharField(max_length=300)    
    subject=models.CharField("Subject", max_length=120)
    message=models.TextField("Personal Message", default='', blank=True)
    
    remote_ip=models.IPAddressField()
    happened_at=models.DateTimeField(editable=False, default=datetime.datetime.now)

    def __unicode__(self):
        return "%s emailed by %s to %s" % (self.content_object,
                                           self.email_from,
                                           self.email_to)