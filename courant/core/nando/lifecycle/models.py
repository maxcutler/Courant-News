from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from courant.core.dynamic_models.models import DynamicModelBase
from courant.core.staff.models import Staffer
from courant.core.news.models import Article
from courant.core.media.models import MediaItem

class Pitch(DynamicModelBase):
	"""
	Story pitch.
	"""
	
	name = models.CharField(max_length=100)
	body = models.TextField()
	
	user = models.OneToOneField(User, blank=True, null=True,
                                help_text="Optional.")
	
	created_at = CreationDateTimeField()
	modified_at = ModificationDateTimeField()
	
	class Meta:
		verbose_name_plural = 'Pitches'
	
class Assignment(DynamicModelBase):
	
	pitches = models.ManyToManyField(Pitch, related_name='assignments')
	
	slug = models.SlugField(unique=True)
	#department after Staff refactor
	published_at = models.DateTimeField()
	
	assigned_to = models.ManyToManyField(Staffer, related_name="assignments")
	body = models.TextField()

	related_assignments = models.ManyToManyField('self', blank=True, null=True, related_name='related_assignments')
	
class ArticleAssignment(Assignment):
	articles = models.ManyToManyField(Article, related_name="assignments")

class MediaAssignment(Assignment):
	media = models.ManyToManyField(MediaItem, related_name="assignments")