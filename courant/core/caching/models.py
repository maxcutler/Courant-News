from django.db import models
from django.db.models.signals import post_save
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import ModificationDateTimeField
from django.conf import settings

# number of seconds to wait before fullpage cache is deleted when expiring a template fragment on that page
FULLPAGE_CACHE_REFRESH = 10

class CachedObject(models.Model):
	cache_key = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	modified_at = ModificationDateTimeField()

def clear_obj_cache(obj):
	try:
		obj_caches = CachedObject.objects.filter(content_type=ContentType.objects.get_for_model(obj),
												 object_id=obj.pk)
		urls = []
		for obj_cache in obj_caches:
			# mark object's cache as stale so it will be safely regenerated
			cache.delete("%s.stale" % obj_cache.cache_key)

			# mark URL as needing cache clearing
			urls.append(obj_cache.url)

		# for full page caches, reset them with a short expiration time.
		# this should hopefully allow for a non-anonymous user to load
		# the page and create template fragment caches, so that when the
		# first anonymous user hits the page, it doesn't have to do much
		# processing to create a new full-page cache (since the fragments are
		# all cached), and thus avoid potential dogpiling
		for url in set(urls):
			key = "%s-%s" % (settings.CACHE_KEY_PREFIX, url)
			fullpage_cache = cache.get(key)
			if fullpage_cache:
				cache.set(key, fullpage_cache, FULLPAGE_CACHE_REFRESH)
	except:
		pass

def clear_obj_cache_signal(sender, instance, **kwargs):
	clear_obj_cache(instance)
post_save.connect(clear_obj_cache_signal)