from django.db.models.signals import pre_init
from courant.core.countthis.models import Statistic
from django.contrib.contenttypes.models import ContentType


def add_statistics(sender, *args, **kwargs):
    sender.add_to_class('statistics',
                        lambda self:
                            Statistic.objects.get(
                                content_type=
                                    ContentType.objects.get_for_model(self),
                                object_id=self.pk))

pre_init.connect(add_statistics)
