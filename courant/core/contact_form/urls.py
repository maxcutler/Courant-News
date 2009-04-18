"""
Taken from Bennett's django-contact-form app
"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from courant.core.contact_form.views import contact_form


urlpatterns = patterns('',
                       url(r'^$',
                           contact_form,
                           name='contact_form'),
                       url(r'^sent/$',
                           direct_to_template,
                           {'template': 'contact_form/contact_form_sent.html'},
                           name='contact_form_sent'),
                       )
