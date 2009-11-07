from django.template import Library, Node, TemplateSyntaxError
from django.template import resolve_variable
from django.core.cache import cache
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType

from courant.core.caching.models import CachedObject

register = Library()


class SmartCacheNode(Node):
    # based on http://www.djangosnippets.org/snippets/614/

    STALE_REFRESH = 1
    STALE_CREATED = 2

    def __init__(self, nodelist, expire_time, fragment_name, vary_on, cache_obj=None):
        self.nodelist = nodelist
        self.stale_time = expire_time
        self.expire_time = expire_time + 300 # create a window to refresh
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        self.cache_obj = cache_obj

    def render(self, context):
        # Build a unicode key for this fragment and all vary-on's.
        cache_key = u':'.join([self.fragment_name] + \
            [force_unicode(resolve_variable(var, context)) for var in self.vary_on])
        cache_key_stale = cache_key + '.stale'
        value = cache.get(cache_key)
        stale = cache.get(cache_key_stale)
        if stale is None:
            cache.set(cache_key_stale, self.STALE_REFRESH, 30) # lock
            value = None # force refresh
        if value is None:
            context.push()
            context['cache_key'] = cache_key
            value = self.nodelist.render(context)
            context.pop()
            cache.set(cache_key, value, self.expire_time)
            cache.set(cache_key_stale, self.STALE_CREATED, self.stale_time)
            if self.cache_obj:
                obj = resolve_variable(self.cache_obj, context)
                co, created = CachedObject.objects.get_or_create(url=context['request'].get_full_path(),
                                                                 content_type=ContentType.objects.get_for_model(obj),
                                                                 object_id=obj.pk,
                                                                 cache_key=cache_key)
                co.save() # update modified timestamp
        return value


def do_smart_cache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time, but with the extra bonus of limiting the dog-pile/stampeding
    effect.

    Usage::

        {% cache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcache %}

    This tag also supports varying by a list of arguments::

        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcache %}

    Each unique set of arguments will result in a unique cache entry.
    
    To enable automatic cache invalidation, a model object can be passed as
    a final optional parameter. Whenever the object is saved, this template
    fragment will be regenerated::
        
        {% cache [expire_time] [fragment_name] [var1] for [obj] %}
            .. some expensive processing ..
        {% endcache %}
        
    See the 'cache_dup' template tag to enable automatic cache invalidation
    based on more than a single object.
    """
    nodelist = parser.parse(('endcache', ))
    parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 3:
        raise TemplateSyntaxError(
            u"'%r' tag requires at least 2 arguments." % tokens[0])
    try:
        expire_time = int(tokens[1])
    except ValueError:
        raise TemplateSyntaxError(
            u"First argument to '%r' must be an integer (got '%s')." %
            (tokens[0], tokens[1]))
    if (tokens[-2] == 'for'):
        return SmartCacheNode(nodelist, expire_time, tokens[2], tokens[3:-2], tokens[-1])
    return SmartCacheNode(nodelist, expire_time, tokens[2], tokens[3:])

register.tag('cache', do_smart_cache)

class CacheDependencyNode(Node):
    def __init__(self, deps):
        self.deps = deps

    def render(self, context):
        if 'cache_key' in context:
            for dep in self.deps:
                obj = resolve_variable(dep, context)
                co, created = CachedObject.objects.get_or_create(url=context['request'].get_full_path(),
                                                                 content_type=ContentType.objects.get_for_model(obj),
                                                                 object_id=obj.pk,
                                                                 cache_key=context['cache_key'])
                co.save() # update modified timestamp
        return ''

def do_cache_dependency(parser, token):
    """
    When used inside a {% cache %} template tag block, this template tag will
    cause the entire cache block to be regenerated whenever any of the passed
    parameters change::
        
        {% cache_dup [var1] %}
        {% cache_dup [var1] [var2] %}
        
    Example usage::
        
        {% cache .. for object_a %}
            .. expensive processing ..
            {% cache_dup object_b %}
            .. more processing ..
            {% cache_dup object_c object _d %}
        {% endcache %}
        
    In this example, when the model objects referred to by 'object_a', 
    'object_b', 'object_c', or 'object_d' are saved, this template fragment
    will be automatically invalidated and regenerated. 
    
    There is no limit to the number of times 'cache_dup' can be called within
    a single 'cache' block.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        return CacheDependencyNode(bits[1:])
    return ''
register.tag('cache_dep', do_cache_dependency)