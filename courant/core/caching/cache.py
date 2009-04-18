"""Wrapper functions around Django's core cache to implement
stale-while-revalidating cache. Has the standard Django cache
interface. The timeout passed to ``set'' is the time at which
the cache will be revalidated; this is different from the
built-in cache behavior because the object will still be available
from the cache for MINT_DELAY additional seconds.
"""

import time

from django.core.cache import cache

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
