from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.contrib.admin import helpers
from django import template

import notifications

def send_email_update(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    app_label = opts.app_label
    template_prefix = opts.object_name.lower()+"s"

    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    if request.POST.get('post'):
         for article in queryset:
            options = {
                'subject': u'YDN Update: %s' % article.heading,
                'from_address': 'headlines@yaledailynews.com',
                'from_name': 'Yale Daily News',
                'data': article,
                'text_template': '%s/email.txt' % template_prefix,
                'html_template': '%s/email.html' % template_prefix,
            }
            count = notifications.send_email_update(**options)
            modeladmin.message_user(request, "Email update submitted. %d emails queued for delivery." % count)

         # Return None to display the change list page again.
         return None

    context = {
        "title": "Are you sure?",
        "object_name": force_unicode(opts.verbose_name),
        'queryset': queryset,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }

    # Display the confirmation page
    return render_to_response([
        "admin/%s/%s/send_email_update.html" % (app_label, opts.object_name.lower()),
        "admin/%s/send_email_update.html" % app_label,
        "admin/send_email_update.html"
    ], context, context_instance=template.RequestContext(request))

send_email_update.short_description = "Send email update"