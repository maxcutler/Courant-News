import logging
from datetime import datetime

from django.conf import settings
from django.core.management.base import NoArgsCommand

from courant.core.mailer.models import Message, MessageJob

class Command(NoArgsCommand):
    help = 'Process a mail job definition to create message jobs for all its recipients.'
    
    def handle_noargs(self, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)

        try:
            msg = MessageJob.objects.filter(processed=False)[0]
        except:
            logging.debug("No new message jobs to process.")
            return # no definitions to process
        
        # set this definition as processed to avoid future invocations
        # of this command stomping on this process and creating duplicates
        # if it takes a long time to process this definition
        msg.processed = True
        msg.save()
        
        logging.info("Processing recipients:")
        count = 0
        for recipient in msg.recipient_list.split(';'):
            options = {
                'to_address': recipient,
                'from_address': msg.from_address,
                'subject': msg.subject,
                'message_body': msg.message_body,
                'message_body_html': msg.message_body_html,
                'priority': msg.priority
            }
            Message(**options).save()
            count += 1
            logging.info("\tSent to %s" % recipient)

        msg.processed_at = datetime.now()
        msg.save()
        
        logging.debug("Message job processed. %d emails queued." % count)