from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('ads/gam/init.html')
def gam_init():
    return {'account_id': settings.GAM_ACCOUNT_ID, 'debug': settings.DEBUG}


@register.inclusion_tag('ads/gam/display_ad.html')
def gam_display_ad(name, width, height):
    return {'name': name, 'width': width, 'height': height,
            'account_id': settings.GAM_ACCOUNT_ID, 'debug': settings.DEBUG}
