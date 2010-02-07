from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

from datetime import datetime

from courant.core.media.models import *
from courant.core.utils import render

from tagging.models import Tag

def media_detailed(request, slug=None, year=None, month=None, day=None, template=None):
    kwargs = { 'slug':slug }
    if year and month and day:
        kwargs['published_at__year'] = int(year)
        kwargs['published_at__month'] = int(month)
        kwargs['published_at__day'] = int(day)
    media_item = MediaItem.objects.get(**kwargs).as_leaf_class()
    return render(request,
                  [template,
                   'media/%s/detailed' % media_item.content_type.name.lower().replace(' ', '_'),
                   'media/detailed'],
                  {'media_item':media_item})
    
def media_archive(request, type, template=None):
    for model in models.get_models():
        if issubclass(model, MediaItem) and not model is MediaItem and model._meta.verbose_name_plural == type:
            template_search = [
                template,
                'media/%s/archive' % model._meta.verbose_name,
                'media/archive',
            ]
            return render(request, template_search, {'model': model, 'model_name': model._meta.verbose_name_plural })
            
    raise Http404