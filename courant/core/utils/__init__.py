from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template import add_to_builtins
from django.db.models.signals import pre_init
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from courant.core.gettag import gettag
from tagging.models import Tag, TaggedItem

def render(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)

    # add appropriate file extension to template list
    arguments = [arg for arg in args]
    templates = []
    for template in arguments[0]:
        if template:
            templates.append(''.join([template, '.', request.extension]))
    arguments[0] = templates

    return render_to_response(*arguments, **kwargs)

#Make common_tags available everywhere
for library in settings.TEMPLATE_TAGS:
    add_to_builtins(library)

#Add a .type method to every object, so you can ask it what type it is from templates
def add_type(sender, *args, **kwargs):
    sender.add_to_class('type', lambda self: self._meta.verbose_name )
pre_init.connect(add_type)

# register Tag model with gettag, since Tag model can't be modified directly (svn:external)
gettag.register(Tag, name_field='tag__name',
                with_func=Tag.objects.usage_for_queryset,
                in_func=TaggedItem.objects.get_by_model)