from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.dispatch import dispatcher
from django.template.defaultfilters import slugify
from django.template import VariableDoesNotExist

import tagging
import datetime
from tagging.fields import TagField

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from comment_utils.moderation import moderator

from djangosphinx.manager import SphinxSearch

from courant.core.staff.models import Staffer, ContentByline
from courant.core.media.models import MediaItem, ContentMedia
from courant.core.discussions.models import CommentOptions, DefaultCommentOption
from courant.core.utils.managers import SubclassManager
from courant.core.gettag import gettag
from courant.core.search import search
from courant.core.discussions.moderation import CourantModerator
from courant.core.dynamic_models.models import DynamicModelBase


class DisplayType(models.Model):
    """
    Specifies a name and template for rendering a specific type or instance of
    a model. 
    """
    name = models.CharField(max_length=40)
    template_name = models.CharField("Template name (without file extension)",
                                     max_length=100)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class ArticleDisplayType(DisplayType):
    """
    Specifies the template used to display a type of article.
    """
    pass


class IssueDisplayType(DisplayType):
    """
    Specifies the template used to display a type of issue.
    """
    pass


class Issue(DynamicModelBase):
    """
    Analog to the print edition of a newspaper or other publication. Specifies
    a collection of content published on a specific day.
    """
    name = models.CharField(max_length=100)
    published = models.BooleanField(default=False,
                                    help_text="Is this currently publicly viewable?")
    display_type = models.ForeignKey(IssueDisplayType)
    
    articles = models.ManyToManyField('Article', through='IssueArticle',
                                      related_name='issues')
    
    lead_media = models.ForeignKey(MediaItem, related_name='issues', blank=True, null=True)

    published_at = models.DateTimeField()
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()

    class Meta:
        ordering = ['-published_at']
        get_latest_by = 'published_at'

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        publish_children_articles = False
        if self.id:
            old_issue = Issue.objects.get(id=self.id)
            if not old_issue.published and self.published:
                publish_children_articles = True
                
        super(Issue, self).save(*args, **kwargs)
        
        if publish_children_articles:
            published_status = ArticleStatus.objects.filter(published=True)[0]
            Article.objects.filter(issues=self).update(status=published_status)
    
    def ordered_articles(self):
        return [x.article for x in IssueArticle.objects.filter(issue=self,
                                                               article__status__published=True,
                                                               article__published_at__lte=datetime.datetime.now()).order_by('order')]
    
    @models.permalink
    def get_absolute_url(self):
        return('issue_archive', (), {
            'year': self.published_at.year,
            'month': '%02d' % self.published_at.month,
            'day': '%02d' % self.published_at.day
        })

    def articles_by_section(self):
        """
        Retrieve all articles for this issue grouped by their sections.
        """
        return Article.objects.filter(issue=self).order_by('section')
gettag.register(Issue)

class IssueArticle(models.Model):
    """
    Connects an article to an issue, including the slot/order in which
    the article should be displayed among all of that issue's articles.
    """
    issue = models.ForeignKey(Issue)
    article = models.ForeignKey('Article')
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
        
    def __unicode__(self):
        return u'%s: %s: %s' % (self.issue, self.article.section, self.article.heading)


class Section(DynamicModelBase):
    """
    A method for organizing content based on their general purpose or topic.
    A section can have an arbitary number of subsections, resulting in a
    tree-like structure. 
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subsections')
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100,
                            help_text="Path added to path of parent section.")
    full_path = models.CharField(max_length=100, editable=False,
                                 blank=True, default='/',
                                 help_text="Full (denormalized) path.")

    class Meta:
        unique_together = ("parent", "path")

    def __unicode__(self):
        return self.name

    def save(self):
        # Denormalization for performance
        self.full_path = self.calculate_full_path()
        
        super(Section, self).save()

        # Re-save subsections to propogate any full path changes
        for subsection in self.subsections.all():
            subsection.save()

    @models.permalink
    def get_absolute_url(self):
        return('section_detailed', (), {
            'path': self.full_path
        })

    def calculate_full_path(self):
        """
        Determines the full path based on the parent section's path.
        """
        if self.parent:
            return self.parent.full_path + '/' + self.path
        else:
            return self.path

    def indented_name(self):
        """
        Only for use in the admin change list to show the tree heirarchy.
        """
        indents = self.full_path.count('/')
        return '-- ' * indents + self.name
    indented_name.short_description = 'Name'

def section_from_name(name):
   if isinstance(name, Section):
      return name
   try:
      section = Section.objects.get(name__iexact=name)
   except (Section.DoesNotExist, Section.MultipleObjectsReturned):
      try:
         section = Section.objects.get(full_path='/'.join(slugify(bit) for bit in name.split('/')))
      except Section.DoesNotExist:
         try:
            section = Section.objects.get(full_path=name.lower())
         except Section.DoesNotExist:
            raise VariableDoesNotExist, "Section '%s' does not exist" % name
   return section

def section_filter(section):
   return ('full_path__startswith',section.full_path)
   
gettag.register(Section, name_field=section_from_name, filter_func=section_filter)

class ArticleStatus(models.Model):
    """
    A status value that can be assigned to an article. Useful for handling
    newsroom workflow, and used to determine which articles are visible on the
    public-facing website.
    """
    name = models.CharField(max_length=100)
    published = models.BooleanField(default=False,
                                    help_text="Is this currently publicly viewable?")

    class Meta:
        verbose_name_plural = "Article Statuses"

    def __unicode__(self):
        return self.name


class ArticleManager(models.Manager):

    def with_media(self):
        return self.get_query_set().filter(media__pk__gt=0)


class LiveArticleManager(models.Manager):

    def get_query_set(self):
        return super(LiveArticleManager, self).get_query_set().filter(status__published=True,
                                                                      published_at__lte=datetime.datetime.now())


class Article(DynamicModelBase):
    """
    An article, blog post, or other piece of text-based content.
    """
    section = models.ForeignKey(Section, related_name="articles")
    display_type = models.ForeignKey(ArticleDisplayType, related_name="articles")
    status = models.ForeignKey(ArticleStatus, related_name="articles")

    authors = models.ManyToManyField(Staffer, through='ArticleByline', related_name='articles')
    media = models.ManyToManyField(MediaItem, through='ArticleMedia', related_name='articles')

    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=255, blank=True)
    summary = models.TextField()
    summary_html = models.TextField(editable=False)
    body = models.TextField()
    body_html = models.TextField(editable=False)

    slug = models.SlugField(unique=True)
    
    correction = models.ForeignKey('self', related_name='corrected', null=True, blank=True)

    published_at = models.DateTimeField()
    content_modified_at = ModificationDateTimeField()
    created_at = CreationDateTimeField()
    modified_at = ModificationDateTimeField()

    tags = TagField()
    
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    
    def default_comment_option():
        try:
            return DefaultCommentOption.objects.get(content_type=ContentType.objects.get_for_model(Article)).options
        except:
            return None

    comment_options = models.ForeignKey(CommentOptions, null=True, default=default_comment_option)

    objects = ArticleManager()
    live = LiveArticleManager()
    search = SphinxSearch('articles_main articles_delta')

    class Meta:
        ordering = ["-published_at", "issuearticle__order"]
        get_latest_by = "-published_at"

    def __unicode__(self):
        return self.heading
    
    def save(self, **kwargs):
        self.body_html = self.body
        super(Article, self).save(**kwargs)
        
    def ordered_media(self):
        return ArticleMedia.objects.filter(article=self).order_by('order')

    @models.permalink
    def get_absolute_url(self):
        return('article_detailed', (), {
            'section': self.section.full_path,
            'slug': self.slug,
            'year': self.published_at.year,
            'month': "%02d" % self.published_at.month,
            'day': "%02d" % self.published_at.day,
        })

    @models.permalink
    def get_comment_url(self):
        return('article_comments', (), {
            'section': self.section.full_path,
            'slug': self.slug,
            'year': self.published_at.year,
            'month': "%02d" % self.published_at.month,
            'day': "%02d" % self.published_at.day,
        })
moderator.register(Article, CourantModerator)
gettag.register(Article, name_field='heading')
search.register(Article,
                fields=('heading', 'subheading', 'summary', 'body'),
                filter_fields=('section', 'display_type','status'),
                date_field='published_at',
                use_delta=True)

class ArticleByline(ContentByline):
    """
    Associates a staffer with an article, including their position and the
    order to display this staffer among all staffers associated with the article.
    """
    article = models.ForeignKey(Article)


class ArticleMedia(ContentMedia):
    """
    Associates a media item with an article, including the order to display
    this media item among all media items associated with the article.
    """
    article = models.ForeignKey(Article)
    
    class Meta:
        ordering = ['order']
