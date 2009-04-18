
from south.db import db
from django.db import models
from courant.core.emailthis.models import *

class Migration:
    
    def forwards(self):
        
        
        # Mock Models
        ContentType = db.mock_model(model_name='ContentType', db_table='django_content_type', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'EmailEvent'
        db.create_table('emailthis_emailevent', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('content_type', models.ForeignKey(ContentType)),
            ('object_id', models.IntegerField()),
            ('mailed_by', models.ForeignKey(User, null=True, blank=True)),
            ('email_from', models.EmailField("Your Email", help_text="required")),
            ('email_to', models.CharField(max_length=300)),
            ('subject', models.CharField("Subject", max_length=120)),
            ('message', models.TextField("Personal Message", blank=True)),
            ('remote_ip', models.IPAddressField()),
            ('happened_at', models.DateTimeField(editable=False, default=datetime.datetime.now)),
        ))
        
        db.send_create_signal('emailthis', ['EmailEvent'])
    
    def backwards(self):
        db.delete_table('emailthis_emailevent')
        
