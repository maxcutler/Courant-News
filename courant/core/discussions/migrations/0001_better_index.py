from south.db import db
from django.db import models


class Migration:

    def forwards(self):
        #db.execute("CREATE INDEX `django_comments_ct_id_pub_rem` ON `django_comments` (`content_type_id`,"
        #           "`object_pk`(5),`is_public`,`is_removed`);")
        db.create_index('django_comments',
                        ['content_type_id', 'object_pk',
                         'is_public', 'is_removed'])

    def backwards(self):
        #db.execute("DROP INDEX `django_comments_ct_id_pub_rem` ON `django_comments`;")
        db.delete_index('django_comments',
                        ['content_type_id', 'object_pk',
                         'is_public', 'is_removed'])
