from django.db import models

from south.db import db

from courant.core.staff.models import *


class Migration:

    def forwards(self):
        # Mock Models
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})

        # Model 'Staffer'
        db.create_table('staff_staffer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.OneToOneField(User, blank=True, null=True, help_text="Optional, but recommended.")),
            ('slug', models.SlugField()),
            ('position', models.CharField(max_length=50)),
            ('first_name', models.CharField(max_length=30, blank=True)),
            ('last_name', models.CharField(max_length=30, blank=True)),
        ))
        db.create_index('staff_staffer', ['first_name', 'last_name'], unique=True, db_tablespace='')


        db.send_create_signal('staff', ['Staffer'])

    def backwards(self):
        db.delete_table('staff_staffer')
