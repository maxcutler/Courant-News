
from south.db import db
from django.db import models
from courant.core.news.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Article.correction_for'
        db.add_column('news_article', 'correction', models.ForeignKey(orm.Article, related_name='corrected', null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Article.correction_for'
        db.delete_column('news_article', 'correction_id')
        
    
    
    models = {
        'media.mediaitem': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.articledisplaytype': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '40'}),
            'template_name': ('models.CharField', ['"Template name (without file extension)"'], {'max_length': '100'})
        },
        'news.section': {
            'Meta': {'unique_together': '("parent","path")'},
            'dynamic_type': ('models.ForeignKey', ["orm['dynamic_models.DynamicType']"], {'default': 'None', 'null': 'True'}),
            'full_path': ('models.CharField', [], {'default': "'/'", 'max_length': '100', 'editable': 'False', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'parent': ('models.ForeignKey', ["orm['news.Section']"], {'related_name': "'subsections'", 'null': 'True', 'blank': 'True'}),
            'path': ('models.CharField', [], {'max_length': '100'})
        },
        'news.issuearticle': {
            'Meta': {'ordering': "['order']"},
            'article': ('models.ForeignKey', ["orm['news.Article']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'issue': ('models.ForeignKey', ["orm['news.Issue']"], {}),
            'order': ('models.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.articlemedia': {
            'Meta': {'ordering': "['order']"},
            'article': ('models.ForeignKey', ["orm['news.Article']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_item': ('models.ForeignKey', ["orm['media.MediaItem']"], {}),
            'order': ('models.PositiveSmallIntegerField', [], {})
        },
        'dynamic_models.dynamictype': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.article': {
            'Meta': {'ordering': '["-published_at","issuearticle__order"]', 'get_latest_by': '"-published_at"'},
            'authors': ('models.ManyToManyField', ["orm['staff.Staffer']"], {'related_name': "'articles'", 'through': "'ArticleByline'"}),
            'body': ('models.TextField', [], {}),
            'body_html': ('models.TextField', [], {'editable': 'False'}),
            'comment_options': ('models.ForeignKey', ["orm['discussions.CommentOptions']"], {'null': 'True'}),
            'content_modified_at': ('ModificationDateTimeField', [], {}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'null': 'True', 'editable': 'False'}),
            'correction': ('models.ForeignKey', ["orm['news.Article']"], {'related_name': "'corrected'", 'null': 'True', 'blank': 'True'}),
            'created_at': ('CreationDateTimeField', [], {}),
            'display_type': ('models.ForeignKey', ["orm['news.ArticleDisplayType']"], {'related_name': '"articles"'}),
            'dynamic_type': ('models.ForeignKey', ["orm['dynamic_models.DynamicType']"], {'default': 'None', 'null': 'True'}),
            'heading': ('models.CharField', [], {'max_length': '255'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media': ('models.ManyToManyField', ["orm['media.MediaItem']"], {'related_name': "'articles'", 'through': "'ArticleMedia'"}),
            'modified_at': ('ModificationDateTimeField', [], {}),
            'published_at': ('models.DateTimeField', [], {}),
            'section': ('models.ForeignKey', ["orm['news.Section']"], {'related_name': '"articles"'}),
            'slug': ('models.SlugField', [], {'unique': 'True'}),
            'status': ('models.ForeignKey', ["orm['news.ArticleStatus']"], {'related_name': '"articles"'}),
            'subheading': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'summary': ('models.TextField', [], {}),
            'summary_html': ('models.TextField', [], {'editable': 'False'}),
            'tags': ('TagField', [], {})
        },
        'news.articlebyline': {
            'article': ('models.ForeignKey', ["orm['news.Article']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'order': ('models.PositiveSmallIntegerField', [], {}),
            'position': ('models.CharField', [], {'max_length': '100'}),
            'staffer': ('models.ForeignKey', ["orm['staff.Staffer']"], {})
        },
        'discussions.commentoptions': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.issue': {
            'Meta': {'ordering': "['-published_at']", 'get_latest_by': "'-published_at'"},
            'articles': ('models.ManyToManyField', ["orm['news.Article']"], {'related_name': "'issues'", 'through': "'IssueArticle'"}),
            'created_at': ('CreationDateTimeField', [], {}),
            'display_type': ('models.ForeignKey', ["orm['news.IssueDisplayType']"], {}),
            'dynamic_type': ('models.ForeignKey', ["orm['dynamic_models.DynamicType']"], {'default': 'None', 'null': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'lead_media': ('models.ForeignKey', ["orm['media.MediaItem']"], {'related_name': "'issues'", 'null': 'True'}),
            'modified_at': ('ModificationDateTimeField', [], {}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'published_at': ('models.DateTimeField', [], {})
        },
        'news.articlestatus': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'published': ('models.BooleanField', [], {'default': 'False'})
        },
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.issuedisplaytype': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '40'}),
            'template_name': ('models.CharField', ['"Template name (without file extension)"'], {'max_length': '100'})
        }
    }
    
    complete_apps = ['news']
