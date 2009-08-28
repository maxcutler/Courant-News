from django.db import models
from django.contrib.auth.models import User
from djangosphinx.manager import SphinxSearch

from courant.core.search import search

class Staffer(models.Model):
    """
    Represents a staff member in the news organization, or anyone who publishes
    content on the web site.
    """
    user = models.OneToOneField(User, blank=True, null=True,
                                help_text="Optional, but recommended.")
    slug = models.SlugField()
    position = models.CharField(max_length=255)

    # denormalization if a user is linked to this staffer, or else holds the
    # staffer's name if they do not have a user account
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    search = SphinxSearch('staffers')

    class Meta:
        ordering = ['user']
        unique_together = ['first_name', 'last_name']

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self):
        if self.user: #denormalization
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        super(Staffer, self).save()

    @models.permalink
    def get_absolute_url(self):
        return('staffer_detailed', (), {'slug': self.slug})
search.register(Staffer,
                fields=('first_name', 'last_name', 'position'),
                date_field=None)

class ContentByline(models.Model):
    """
    Abstract base class that handles associating staffers with other types
    of content.
    """
    staffer = models.ForeignKey(Staffer)
    position = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s - %s" % (self.staffer, self.position)

    def save(self):
        # denormaliaze position, since a staffer's position may change year-to-year
        # but the position field should only reflect their position at time of
        # publication
        self.position = self.staffer.position
        super(ContentByline, self).save()
