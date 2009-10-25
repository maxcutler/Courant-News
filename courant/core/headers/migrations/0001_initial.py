
from south.db import db
from django.db import models
from courant.core.headers.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'HttpHeader'
        db.create_table('headers_httpheader', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
            ('header', models.CharField(max_length=50)),
            ('description', models.TextField()),
        ))
        db.send_create_signal('headers', ['HttpHeader'])
        
        # Adding model 'HeaderRule'
        db.create_table('headers_headerrule', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
            ('header', models.ForeignKey(orm.HttpHeader)),
            ('domain', models.CharField(max_length=50)),
            ('regex', models.CharField(max_length=255)),
            ('extension_list', models.CharField(max_length=50)),
            ('context_var', models.CharField(max_length=50)),
            ('order', models.PositiveSmallIntegerField()),
            ('enabled', models.BooleanField('Enable This Rule')),
            ('admin_override', models.BooleanField('Enable This Rule for Admins for Testing')),
        ))
        db.send_create_signal('headers', ['HeaderRule'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'HttpHeader'
        db.delete_table('headers_httpheader')
        
        # Deleting model 'HeaderRule'
        db.delete_table('headers_headerrule')
        
    
    
    models = {
        'headers.httpheader': {
            'description': ('models.TextField', [], {}),
            'header': ('models.CharField', [], {'max_length': '50'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'})
        },
        'headers.headerrule': {
            'admin_override': ('models.BooleanField', ["'Enable This Rule for Admins for Testing'"], {}),
            'context_var': ('models.CharField', [], {'max_length': '50'}),
            'domain': ('models.CharField', [], {'max_length': '50'}),
            'enabled': ('models.BooleanField', ["'Enable This Rule'"], {}),
            'extension_list': ('models.CharField', [], {'max_length': '50'}),
            'header': ('models.ForeignKey', ["orm['headers.HttpHeader']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'}),
            'order': ('models.PositiveSmallIntegerField', [], {}),
            'regex': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['headers']
