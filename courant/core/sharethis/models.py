from django.db import models


class SocialNetwork(models.Model):
    name = models.CharField(max_length=100)
    code = models.TextField()
    enabled = models.BooleanField()

    def __unicode__(self):
        return self.name
