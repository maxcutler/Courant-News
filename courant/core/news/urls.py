from django.conf.urls.defaults import *
from courant.core.news.views import *

urlpatterns = patterns('',
    url(r'^$', homepage, name="homepage"),
    url(r'^latest/$', homepage, name="homepage_rss"),

    url(r'^tags/(?P<tag_name>[-.\' \w\/]+)/$', tag_detailed, name="tag_detailed"),
    url(r'^issues/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',issue_archive, name="issue_archive"),
    url(r'^(?P<section>[-\w\/]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', article_detailed,name="article_detailed"),
    url(r'^(?P<section>[-\w\/]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/comments/$', article_detailed, {'template': 'articles/comments'},name="article_comments"),
    url(r'(?P<path>.*)/$', section_detailed, name="section_detailed"),
)