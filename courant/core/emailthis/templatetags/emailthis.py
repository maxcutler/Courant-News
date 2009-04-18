from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('loadform.html')
def emailthis_loadform(object, div_id="emailthis_form"):
    return {'div_id':div_id, 'object': object }

#Based on http://code.google.com/p/django-mailfriend/source/browse/trunk/mailfriend/templatetags/mailfriend.py
@register.simple_tag
def get_emailthis_url(obj):
  if hasattr(obj, 'get_absolute_url'):
    try:
      content_type = ContentType.objects.get(app_label=obj._meta.app_label, model=obj._meta.module_name)
      return reverse('courant.core.emailthis.views.get_email_form', args=[ content_type.id, obj.id ])
    except:
      return ''
  else:
    return ''