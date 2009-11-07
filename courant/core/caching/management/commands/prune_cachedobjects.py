import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import NoArgsCommand

from courant.core.caching.models import CachedObject

class Command(NoArgsCommand):
    help = 'Prunes old CachedObjects that have been orphaned.'

    def handle_noargs(self, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")

        PRUNE_HOURS = 24

        CachedObject.objects.filter(modified_at__lte=datetime.now()-timedelta(hours=PRUNE_HOURS)).delete()

        logging.debug("Old CachedObjects pruned")