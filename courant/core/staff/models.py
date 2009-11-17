from django.db import models
from django.contrib.auth.models import User

from courant.core.gettag import gettag

from datetime import date

class StaffPositionTitle(models.Model):

	name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name
	
class StaffDepartment(models.Model):

	name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name

class StaffPositionManager(models.Manager):
	use_for_related_fields = True

	def active(self):
		return self.get_query_set().filter(start_on__lte=date.today(), end_on__gte=date.today())

class StaffPosition(models.Model):

	name = models.CharField(max_length=255)
	
	title = models.ForeignKey(StaffPositionTitle)
	position = models.ForeignKey(StaffDepartment)
	
	start_on = models.DateField()
	end_on = models.DateField()
	
	objects = StaffPositionManager()
	
	def __unicode__(self):
		return self.name

class Staffer(models.Model):
	"""
	Represents a staff member in the news organization, or anyone who publishes
	content on the web site.
	"""
	slug = models.SlugField()
	
	user = models.OneToOneField(User, blank=True, null=True,
								help_text="Optional, but recommended.")
	positions = models.ManyToManyField(StaffPosition)

	# denormalization if a user is linked to this staffer, or else holds the
	# staffer's name if they do not have a user account
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	
	bio = models.TextField()
	public_profile = models.BooleanField(default=True)

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
gettag.register(Staffer)

class ContentByline(models.Model):
	"""
	Abstract base class that handles associating staffers with other types
	of content.
	"""
	staffer = models.ForeignKey(Staffer)
	position = models.ForeignKey(StaffPosition)
	order = models.PositiveSmallIntegerField()

	class Meta:
		abstract = True

	def __unicode__(self):
		return "%s - %s" % (self.staffer, self.position)
