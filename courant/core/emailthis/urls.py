from django.conf.urls.defaults import patterns, url

urlpatterns=patterns('courant.core.emailthis.views',
    url(r'^(\d+)/(\d+)/$', 'get_email_form', name="emailthis_form"),
    url(r'^submit/(\d+)/(\d+)/$', 'process_email_form', name="emailthis_submit")
    )
