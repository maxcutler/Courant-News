"""Wrapper functions around Django's core cache to implement
stale-while-revalidating cache. Has the standard Django cache
interface. The timeout passed to ``set'' is the time at which
the cache will be revalidated; this is different from the
built-in cache behavior because the object will still be available
from the cache for MINT_DELAY additional seconds.
"""

import time

from django.core.cache import cache
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType

from models import CachedObject

# based on http://www.djangosnippets.org/snippets/793/
# MINT_DELAY is an upper bound on how long any value should take to
# be generated (in seconds)
MINT_DELAY = 30
DEFAULT_TIMEOUT = 300


def get(key):
    packed_val = cache.get(key)
    if packed_val is None:
        return None
    val, refresh_time, refreshed = packed_val
    if (time.time() > refresh_time) and not refreshed:
        # Store the stale value while the cache revalidates for another
        # MINT_DELAY seconds.
        set(key, val, timeout=MINT_DELAY, refreshed=True)
        return None
    return val


def set(key, val, timeout=DEFAULT_TIMEOUT, refreshed=False):
    refresh_time = timeout + time.time()
    real_timeout = timeout + MINT_DELAY
    packed_val = (val, refresh_time, refreshed)
    return cache.set(key, packed_val, real_timeout)

delete = cache.delete

# utility functions

STALE_REFRESH = 1
STALE_CREATED = 2

def check_smart_cache(request, *args):
    cache_key = u':'.join([force_unicode(arg) for arg in args])
    cache_key_stale = cache_key + '.stale'
    value = cache.get(cache_key)
    stale = cache.get(cache_key_stale)
    if stale is None:
        cache.set(cache_key_stale, STALE_REFRESH, 30) # lock
        value = None # force refresh
    return (value, cache_key)

def update_cache_dependency(request, obj, cache_key):
    if obj:
        co, created = CachedObject.objects.get_or_create(url=request.get_full_path(),
                                                         content_type=ContentType.objects.get_for_model(obj),
                                                         object_id=obj.pk,
                                                         cache_key=cache_key)
        co.save() # update modified timestamp