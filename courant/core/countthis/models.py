from django.db import models, IntegrityError
from django.db.models import F
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import CreationDateTimeField

from courant.core.emailthis.models import EmailEvent, email_sent
from django.contrib.comments.signals import comment_was_posted
from django.contrib.comments.models import Comment


class Statistic(models.Model):
    """
    Tracks various metrics for content objects.
    """
    path = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField()
    view_count = models.PositiveIntegerField(default=0)
    email_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    created_at = CreationDateTimeField()

    class Meta:
        unique_together = ['content_type', 'object_id']

    def __unicode__(self):
        return self.path + str(self.content_object)


def update_count(sender, **kwargs):
    if sender == EmailEvent:
        count_type = 'email_count'
        update = None
    elif sender == Comment:
        kwargs['instance'] = kwargs['comment'].content_object
        count_type = 'comment_count'

        #Get comment count
        count = Comment.objects.for_model(kwargs['instance']).filter(is_public=True, is_removed=False).count()
        update = ''.join(['comment_count=', str(count)])
    else:
        raise Exception('Unsupported model to count.')

    path = kwargs['instance'].get_absolute_url()
    content_type_id = ContentType.objects.get_for_model(kwargs['instance']).pk
    object_id = kwargs['instance'].id

    do_update_count(path, content_type_id, object_id, count_type, update)
email_sent.connect(update_count, sender=EmailEvent)
comment_was_posted.connect(update_count, sender=Comment)


def do_update_count(path, content_type_id, object_id, count_type, update=None):
    if not update:
        update = ''.join([count_type, "=", count_type, "+1"])

    if settings.DATABASE_ENGINE == 'mysql':
        # optimized for MySQL, which supports the ON DUPLICATE KEY UPDATE clause
        from django.db import connection
        cursor = connection.cursor()

        #We have to build this query in two parts. We have to put the count in first, outside of cursor.execute.
        #Otherwise it will wrap the field name in single quotes and cause a SQL error.
        query = ''.join(["INSERT INTO countthis_statistic VALUES(NULL, %s, %s, %s, 1, NOW(), 1, 1) ON DUPLICATE KEY UPDATE ", update])
        cursor.execute(query, [path, content_type_id, object_id])
    else:
        # generic method for database engines that don't support single-query updates
        update_params = {}
        update_params[str(count_type)] = F(count_type)+1
        rows_affected = Statistic.objects.filter(path=path).update(**update_params)
        if rows_affected == 0:
            # object not in the statistics table, so we need to add it
            s = Statistic(path=path,
                          content_type_id=content_type_id,
                          object_id=object_id)
            s.save()
            # after we created the new entry, try to update it again. because
            # of potential race conditions, we avoid setting the +1 value in the
            # creation step
            rows_affected = Statistic.objects.filter(path=path).update(**update_params)

def update_path(sender, instance, **kwargs):
    # if an object's URL changes, then a new Statistic object wlil be created
    # for it when updating a count. therefore, we want to always make sure
    # the correct path is saved for its corresponding Statistic object
    # (if one exists) to avoid duplicates (which will break functionality elsewhere)
    if hasattr(instance, 'get_absolute_url'):
        Statistic.objects.filter(content_type=ContentType.objects.get_for_model(sender), object_id=instance.pk).update(path=instance.get_absolute_url())
post_save.connect(update_path)