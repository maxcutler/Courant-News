
from south.db import db
from django.db import models
from courant.core.news.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Section'
        db.create_table('news_section', (
            ('path', models.CharField(max_length=100)),
            ('full_path', models.CharField(default='/', max_length=100, editable=False, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('parent', models.ForeignKey('self', related_name='subsections', null=True, blank=True)),
            ('name', models.CharField(max_length=100)),
        ))
        db.send_create_signal('news', ['Section'])
        
        # Adding model 'ArticleDisplayType'
        db.create_table('news_articledisplaytype', (
            ('template_name', models.CharField("Template name (without file extension)", max_length=100)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=40)),
        ))
        db.send_create_signal('news', ['ArticleDisplayType'])
        
        # Adding model 'IssueArticle'
        db.create_table('news_issuearticle', (
            ('article', models.ForeignKey(orm.Article)),
            ('issue', models.ForeignKey(orm.Issue)),
            ('id', models.AutoField(primary_key=True)),
            ('order', models.PositiveIntegerField()),
        ))
        db.send_create_signal('news', ['IssueArticle'])
        
        # Adding model 'ArticleMedia'
        db.create_table('news_articlemedia', (
            ('article', models.ForeignKey(orm.Article)),
            ('media_item', models.ForeignKey(orm['media.MediaItem'])),
            ('id', models.AutoField(primary_key=True)),
            ('order', models.PositiveSmallIntegerField()),
        ))
        db.send_create_signal('news', ['ArticleMedia'])
        
        # Adding model 'IssueDisplayType'
        db.create_table('news_issuedisplaytype', (
            ('template_name', models.CharField("Template name (without file extension)", max_length=100)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=40)),
        ))
        db.send_create_signal('news', ['IssueDisplayType'])
        
        # Adding model 'ArticleByline'
        db.create_table('news_articlebyline', (
            ('position', models.CharField(max_length=100)),
            ('article', models.ForeignKey(orm.Article)),
            ('staffer', models.ForeignKey(orm['staff.Staffer'])),
            ('id', models.AutoField(primary_key=True)),
            ('order', models.PositiveSmallIntegerField()),
        ))
        db.send_create_signal('news', ['ArticleByline'])
        
        # Adding model 'Issue'
        db.create_table('news_issue', (
            ('name', models.CharField(max_length=100)),
            ('created_at', CreationDateTimeField()),
            ('modified_at', ModificationDateTimeField()),
            ('published_at', models.DateTimeField()),
            ('display_type', models.ForeignKey(orm.IssueDisplayType)),
            ('published', models.BooleanField(default=False)),
            ('id', models.AutoField(primary_key=True)),
            ('lead_media', models.ForeignKey(orm['media.MediaItem'], related_name='issues', null=True)),
        ))
        db.send_create_signal('news', ['Issue'])
        
        # Adding model 'ArticleStatus'
        db.create_table('news_articlestatus', (
            ('published', models.BooleanField(default=False)),
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=100)),
        ))
        db.send_create_signal('news', ['ArticleStatus'])
        
        # Adding model 'Article'
        db.create_table('news_article', (
            ('status', models.ForeignKey(orm.ArticleStatus, related_name="articles")),
            ('body', models.TextField()),
            ('slug', models.SlugField(unique=True)),
            ('tags', TagField()),
            ('comment_options', models.ForeignKey(orm['discussions.CommentOptions'], default=default_comment_option, null=True)),
            ('modified_at', ModificationDateTimeField()),
            ('section', models.ForeignKey(orm.Section, related_name="articles")),
            ('summary_html', models.TextField(editable=False)),
            ('body_html', models.TextField(editable=False)),
            ('subheading', models.CharField(max_length=255, blank=True)),
            ('id', models.AutoField(primary_key=True)),
            ('content_modified_at', ModificationDateTimeField()),
            ('published_at', models.DateTimeField()),
            ('display_type', models.ForeignKey(orm.ArticleDisplayType, related_name="articles")),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], null=True, editable=False)),
            ('created_at', CreationDateTimeField()),
            ('summary', models.TextField()),
            ('heading', models.CharField(max_length=255)),
        ))
        db.send_create_signal('news', ['Article'])
        
        # Adding ManyToManyField 'Article.media'
        db.create_table('news_articlemedia', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(Article, null=False)),
            ('media_item', models.ForeignKey(MediaItem, null=False))
        ))
        
        # Adding ManyToManyField 'Article.authors'
        db.create_table('news_articlebyline', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(Article, null=False)),
            ('staffer', models.ForeignKey(Staffer, null=False))
        ))
        
        # Adding ManyToManyField 'Issue.articles'
        db.create_table('news_issuearticle', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(Issue, null=False)),
            ('article', models.ForeignKey(Article, null=False))
        ))
        
    
    
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
        
        # Dropping ManyToManyField 'Article.media'
        db.delete_table('news_articlemedia')
        
        # Dropping ManyToManyField 'Article.authors'
        db.delete_table('news_articlebyline')
        
        # Dropping ManyToManyField 'Issue.articles'
        db.delete_table('news_issuearticle')
        
    
    
    models = {
        'media.mediaitem': {
            'Meta': {'ordering': '["-created_at"]', 'get_latest_by': '"-created_at"'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.articledisplaytype': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.section': {
            'Meta': {'unique_together': '("parent","path")'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.issuedisplaytype': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'discussions.commentoptions': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.issue': {
            'Meta': {'ordering': "['-published_at']", 'get_latest_by': "'-published_at'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.articlestatus': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'staff.staffer': {
            'Meta': {'ordering': "['user']", 'unique_together': "['first_name','last_name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'news.article': {
            'Meta': {'ordering': '["-published_at","issuearticle__order"]', 'get_latest_by': '"-published_at"'},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    
