
from south.db import db
from django.db import models

class Migration:
    
    def forwards(self):
        
        # Model for tracking delta indexes - see http://www.sphinxsearch.com/docs/manual-0.9.8.html#live-updates
        db.create_table('sphinx_counter', (
            ('counter_id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('max_doc_id', models.IntegerField()),
        ))
        
        db.send_create_signal('search', ['sphinx_counter'])
    
    def backwards(self):
        db.delete_table('events_event')
        
