from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.contrib.admin import helpers
from django import template

import notifications

def show_email_confirmation_page(modeladmin, request, queryset, action):
    opts = modeladmin.model._meta
    app_label = opts.app_label

    context = {
        "title": "Are you sure?",
        "object_name": force_unicode(opts.verbose_name),
        'queryset': queryset,
        "opts": opts,
        "root_path": modeladmin.admin_site.root_path,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'action': action,
    }

    # Display the confirmation page
    return render_to_response([
        "admin/%s/%s/send_email_update.html" % (app_label, opts.object_name.lower()),
        "admin/%s/send_email_update.html" % app_label,
        "admin/send_email_update.html"
    ], context, context_instance=template.RequestContext(request))

def send_article_email_update(modeladmin, request, queryset):
    # The user has already confirmed the email update.
    # Queue the emails and return a None to display the change list view again.
    if request.POST.get('post'):
         for article in queryset:
            options = {
                'subject': u'YDN Update: %s' % article.heading,
                'from_address': 'headlines@yaledailynews.com',
                'from_name': 'Yale Daily News',
                'data': article,
                'text_template': 'articles/email.txt',
                'html_template': 'articles/email.html',
            }
            count = notifications.send_email_update(**options)
            modeladmin.message_user(request, "Email update submitted. %d emails queued for delivery." % count)

         # Return None to display the change list page again.
         return None

    return show_email_confirmation_page(modeladmin, request, queryset, 'send_article_email_update')
send_article_email_update.short_description = "Send email update"

def send_issue_email_update(modeladmin, request, queryset):
    # The user has already confirmed the email update.
    # Queue the emails and return a None to display the change list view again.
    if request.POST.get('post'):
         for issue in queryset:
            options = {
                'subject': u'YDN Headlines: %s' % (issue.published_at.strftime("%B %d, %Y")),
                'from_address': 'headlines@yaledailynews.com',
                'from_name': 'Yale Daily News',
                'data': issue,
                'text_template': 'issues/email.txt',
                'html_template': 'issues/email.html',
            }
            count = notifications.send_email_update(**options)
            modeladmin.message_user(request, "Email update submitted. %d emails queued for delivery." % count)

         # Return None to display the change list page again.
         return None

    return show_email_confirmation_page(modeladmin, request, queryset, 'send_issue_email_update')
send_issue_email_update.short_description = "Send email update"
