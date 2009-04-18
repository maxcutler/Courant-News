import datetime
import httplib
import logging
import re

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import Http404, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader

from courant.core.emailthis.forms import EmailEventForm
from courant.core.emailthis.models import EmailEvent, email_sent
from courant.core.emailthis.util import render_to_json, get_subject, clean_errors

def get_email_form(request, content_type_id, object_id):
    """
    returns an html form suitable for the specified object.
    """

    try:
        content_type=ContentType.objects.get(pk=content_type_id)
    except ObjectDoesNotExist:
        raise Http404("no such content type")
    try:
        item=content_type.get_object_for_this_type(pk=object_id)

    except ObjectDoesNotExist:
        raise Http404("no such object id")
    subject=get_subject(item)
    user=request.user if request.user.is_authenticated() else None
    initial={'subject' : subject}
    if user and user.email:
        initial['email_from']=user.email
        
    d={'form' : EmailEventForm(initial=initial),
       'item' : item,
       'content_type' : content_type}
    return render_to_response('form.html', d, context_instance=RequestContext(request))


def process_email_form(request, content_type_id=None, object_id=None):
    """
    submission processor for email form.
    """
    if not (request.method=='POST' and request.is_ajax()):
        return HttpResponse('Method Not Allowed', status=httplib.METHOD_NOT_ALLOWED, mimetype='text/plain')
    if content_type_id is None:
        content_type_id=request.POST.get('content_type')
    try:
        content_type=ContentType.objects.get(pk=int(content_type_id))
    except (ObjectDoesNotExist, ValueError, TypeError):
        return HttpResponseBadRequest("invalid content type", mimetype='text/plain')
    if object_id is None:
        object_id=request.POST.get('object_id')
    try:
        item=content_type.get_object_for_this_type(pk=int(object_id))
    except (ObjectDoesNotExist, ValueError, TypeError):
        return HttpResponseBadRequest("no such object id")

    form=EmailEventForm(request.POST)
    if not form.is_valid():
        logging.debug("form is invalid.  Errors are: %s", form.errors)
        logging.debug("type of errors: %s", type(form.errors))
        return render_to_json(clean_errors(form.errors), status=httplib.BAD_REQUEST)
    
    cleaned=form.cleaned_data
    message_template=loader.get_template('email_message.txt')
    site=Site.objects.get_current()
    user=request.user if request.user.is_authenticated() else None    
    message_context=Context(dict(
        email_from=cleaned['email_from'],
        subject=cleaned['subject'],
        message=cleaned['message'],
        site=site,
        site_url='http://%s/' % site.domain,
        url='http://%s%s' % (site.domain, item.get_absolute_url()),
        item=item,
        user=user,
        ))
    message=message_template.render(message_context)
    
    recipients=cleaned['email_to'].split(',')
    from_address=cleaned['email_from']
    send_mail(cleaned['subject'], message, from_address, recipients, fail_silently=False)
    
    #Update email_count
    email_sent.send(sender=EmailEvent, instance=item)
    
    event=form.save(commit=False)
    event.remote_ip=request.META['REMOTE_ADDR']
    event.content_type_id=content_type.pk
    event.object_id=item.pk
    event.mailed_by=user
    event.save()
    return HttpResponse("OK", mimetype="text/plain")

try:
    from djangologging.decorators import suppress_logging_output
except ImportError:
    pass
else:
    get_email_form=suppress_logging_output(get_email_form)
    process_email_form=suppress_logging_output(process_email_form)
    
