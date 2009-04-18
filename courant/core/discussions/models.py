from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from courant.core.gettag import gettag


class CommentOptions(models.Model):
    """
    A collection of settings that governs how comments are moderated or treated.
    """
    name = models.CharField(max_length=50)
    allow_anonymous = models.BooleanField(help_text="Allow anonymous users to post comments")
    moderate_anonymous_only = models.BooleanField(help_text="If set, only anonymous users' comments will be moderated. Authenticated users comments will immediately become publicly visible")
    moderate_after = models.PositiveSmallIntegerField(default=30,
                                                      help_text="# of days after which posts must be moderated. Set to zero (0) for all posts to be moderated")
    close_after = models.PositiveSmallIntegerField(default=365, help_text="# of days after which commenting will be closed. Set to zero (0) to disable commenting")

    class Meta:
        verbose_name = "Comment Options"
        verbose_name_plural = "Comments Options"

    def __unicode__(self):
        return self.name


class DefaultCommentOption(models.Model):
    """
    Assigns a default CommentOptions instance for a given ContentType.
    """
    content_type = models.ForeignKey(ContentType, unique=True)
    options = models.ForeignKey(CommentOptions)

    def __unicode__(self):
        return self.content_type.name

gettag.register(Comment, name_field='body')
