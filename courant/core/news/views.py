from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.flatpages.views import flatpage

from datetime import datetime

from courant.core.utils import render
from courant.core.news.models import *

from tagging.models import Tag


def article_detailed(request, section=None, slug=None, year=None, month=None, day=None, template=None):
    kwargs = {'section__full_path': section,
              'slug': slug}
    if year and month and day:
        kwargs['published_at__year'] = int(year)
        kwargs['published_at__month'] = int(month)
        kwargs['published_at__day'] = int(day)
    if not request.user.is_superuser:
        kwargs['status__published'] = True
    article = Article.objects.get(**kwargs)
    return render(request, [template, 'articles/%s/%s' % (article.section.path, article.display_type.template_name), 'articles/%s' % article.display_type.template_name], {'article': article})


def homepage(request):
    try:
        issue = Issue.objects.filter(published=True).latest('published_at')
        return render(request, ['homepage/%s' % issue.display_type.template_name, 'homepage/default'], {'issue': issue})
    except Issue.DoesNotExist:
        return render(request, ['homepage/default'])


def issue_archive(request, year, month, day):
    issue = Issue.objects.get(published_at__year=int(year),
                              published_at__month=int(month),
                              published_at__day=int(day))
    return render(request, ['issues/archive'], {'issue': issue})


def section_detailed(request, path):
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path[:-1]
    section = get_object_or_404(Section, full_path=path)

    template_search = ["sections/%s/detailed" % path, ]
    while path.count('/') > 0:
        path = path[:path.rfind('/')]
        template_search.append("sections/%s/subsection_detailed" % path)
        template_search.append("sections/%s/detailed" % path)
    template_search.append("sections/detailed")

    return render(request, template_search, {'section': section})


def tag_detailed(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    return render(request, ['tags/custom/%s' % tag_name, 'tags/detailed'], {'tag': tag})
