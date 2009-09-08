
from south.db import db
from django.db import models
from courant.core.news.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Section'
        db.create_table('news_section', (
            ('id', models.AutoField(primary_key=True)),
            ('dynamic_type', models.ForeignKey(orm['dynamic_models.DynamicType'], default=None, null=True)),
            ('parent', models.ForeignKey(orm.Section, related_name='subsections', null=True, blank=True)),
            ('name', models.CharField(max_length=100)),
            ('path', models.CharField(max_length=100)),
            ('full_path', models.CharField(default='/', max_length=100, editable=False, blank=True)),
        ))
        db.send_create_signal('news', ['Section'])
        
        # Adding model 'ArticleDisplayType'
        db.create_table('news_articledisplaytype', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=40)),
            ('template_name', models.CharField("Template name (without file extension)", max_length=100)),
        ))
        db.send_create_signal('news', ['ArticleDisplayType'])
        
        # Adding model 'IssueArticle'
        db.create_table('news_issuearticle', (
            ('id', models.AutoField(primary_key=True)),
            ('issue', models.ForeignKey(orm.Issue)),
            ('article', models.ForeignKey(orm.Article)),
            ('order', models.PositiveIntegerField()),
        ))
        db.send_create_signal('news', ['IssueArticle'])
        
        # Adding model 'ArticleMedia'
        db.create_table('news_articlemedia', (
            ('id', models.AutoField(primary_key=True)),
            ('media_item', models.ForeignKey(orm['media.MediaItem'])),
            ('order', models.PositiveSmallIntegerField()),
            ('article', models.ForeignKey(orm.Article)),
        ))
        db.send_create_signal('news', ['ArticleMedia'])
        
        # Adding model 'IssueDisplayType'
        db.create_table('news_issuedisplaytype', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=40)),
            ('template_name', models.CharField("Template name (without file extension)", max_length=100)),
        ))
        db.send_create_signal('news', ['IssueDisplayType'])
        
        # Adding model 'ArticleByline'
        db.create_table('news_articlebyline', (
            ('id', models.AutoField(primary_key=True)),
            ('staffer', models.ForeignKey(orm['staff.Staffer'])),
            ('position', models.CharField(max_length=100)),
            ('order', models.PositiveSmallIntegerField()),
            ('article', models.ForeignKey(orm.Article)),
        ))
        db.send_create_signal('news', ['ArticleByline'])
        
        # Adding model 'Issue'
        db.create_table('news_issue', (
            ('id', models.AutoField(primary_key=True)),
            ('dynamic_type', models.ForeignKey(orm['dynamic_models.DynamicType'], default=None, null=True)),
            ('name', models.CharField(max_length=100)),
            ('published', models.BooleanField(default=False)),
            ('display_type', models.ForeignKey(orm.IssueDisplayType)),
            ('lead_media', models.ForeignKey(orm['media.MediaItem'], related_name='issues', null=True)),
            ('published_at', models.DateTimeField()),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
        ))
        db.send_create_signal('news', ['Issue'])
        
        # Adding model 'ArticleStatus'
        db.create_table('news_articlestatus', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=100)),
            ('published', models.BooleanField(default=False)),
        ))
        db.send_create_signal('news', ['ArticleStatus'])
        
        # Adding model 'Article'
        db.create_table('news_article', (
            ('id', models.AutoField(primary_key=True)),
            ('dynamic_type', models.ForeignKey(orm['dynamic_models.DynamicType'], default=None, null=True)),
            ('section', models.ForeignKey(orm.Section, related_name="articles")),
            ('display_type', models.ForeignKey(orm.ArticleDisplayType, related_name="articles")),
            ('status', models.ForeignKey(orm.ArticleStatus, related_name="articles")),
            ('heading', models.CharField(max_length=255)),
            ('subheading', models.CharField(max_length=255, blank=True)),
            ('summary', models.TextField()),
            ('summary_html', models.TextField(editable=False)),
            ('body', models.TextField()),
            ('body_html', models.TextField(editable=False)),
            ('slug', models.SlugField(unique=True)),
            ('published_at', models.DateTimeField()),
            ('content_modified_at', ModificationDateTimeField()),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
            ('tags', TagField()),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], null=True, editable=False)),
            ('comment_options', models.ForeignKey(orm['discussions.CommentOptions'], default=default_comment_option, null=True)),
        ))
        db.send_create_signal('news', ['Article'])
        
        # Creating unique_together for [parent, path] on Section.
        db.create_unique('news_section', ['parent_id', 'path'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Section'
        db.delete_table('news_section')
        
        # Deleting model 'ArticleDisplayType'
        db.delete_table('news_articledisplaytype')
        
        # Deleting model 'IssueArticle'
        db.delete_table('news_issuearticle')
        
        # Deleting model 'ArticleMedia'
        db.delete_table('news_articlemedia')
        
        # Deleting model 'IssueDisplayType'
        db.delete_table('news_issuedisplaytype')
        
        # Deleting model 'ArticleByline'
        db.delete_table('news_articlebyline')
        
        # Deleting model 'Issue'
        db.delete_table('news_issue')
        
        # Deleting model 'ArticleStatus'
        db.delete_table('news_articlestatus')
        
        # Deleting model 'Article'
        db.delete_table('news_article')
        
        # Deleting unique_together for [parent, path] on Section.
        db.delete_unique('news_section', ['parent_id', 'path'])
        
    
    
    models = {
        'media.mediaitem': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'dynamic_models.dynamictype': {
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
        'news.articlemedia': {
            'Meta': {'ordering': "['order']"},
            'article': ('models.ForeignKey', ["orm['news.Article']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_item': ('models.ForeignKey', ["orm['media.MediaItem']"], {}),
            'order': ('models.PositiveSmallIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.article': {
            'Meta': {'ordering': '["-published_at","issuearticle__order"]', 'get_latest_by': '"-published_at"'},
            'authors': ('models.ManyToManyField', ["orm['staff.Staffer']"], {'related_name': "'articles'", 'through': "'ArticleByline'"}),
            'body': ('models.TextField', [], {}),
            'body_html': ('models.TextField', [], {'editable': 'False'}),
            'comment_options': ('models.ForeignKey', ["orm['discussions.CommentOptions']"], {'default': 'default_comment_option', 'null': 'True'}),
            'content_modified_at': ('ModificationDateTimeField', [], {}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'null': 'True', 'editable': 'False'}),
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
