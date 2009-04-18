from south.db import db
from django.db import models
from courant.core.sharethis.models import *


class Migration:

    def forwards(self):
        # Model 'SocialNetwork'
        db.create_table('sharethis_socialnetwork', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=100)),
            ('code', models.TextField()),
            ('enabled', models.BooleanField()),
        ))

        db.send_create_signal('sharethis', ['SocialNetwork'])

    def backwards(self):
        db.delete_table('sharethis_socialnetwork')
