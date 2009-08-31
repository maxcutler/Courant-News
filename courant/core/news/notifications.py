from django.template.loader import render_to_string

from courant.core.mailer.models import MessageJob
try:
	from apps.email_subscriptions.models import EmailSubscription
except:
	pass
from courant.core.profiles.models import UserProfile
from models import *

def send_email_update(subject, from_address, from_name, data, html_template=None, text_template=None):
    raw_subscriptions = EmailSubscription.objects.all().values_list('email', flat=True)
    subscribed_users = UserProfile.objects.filter(subscribed=True).values_list('user__email', flat=True)
    recipient_list = list(set(raw_subscriptions) | set(subscribed_users)) # union
    
    msg = MessageJob(from_address='%s <%s>' % (from_name, from_address),
                     subject=subject,
                     recipient_list=';'.join(recipient_list))
    msg.message_body = render_to_string(text_template, {'data': data})
        
    if html_template:
            msg.message_body_html = render_to_string(html_template, {'data': data})
            
    msg.save()
    
    return len(recipient_list)
