from django import template
from django.conf import settings
import random

register = template.Library()

@register.inclusion_tag('ads/openx/display_ad.html')
def openx_display_ad(zone, width, height):
    return {'zone': zone, 'width': width, 'height': height,
            'openx_url': settings.OPENX_URL, 'debug': settings.DEBUG,
            'rand1': random.randrange(99999999),
            'rand2': random.randrange(99999999),}
