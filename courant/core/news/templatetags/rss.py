from django import template

register = template.Library()


@register.inclusion_tag('articles/article_list.rss', takes_context=True)
def rss_article_items(context, articles):
    return {'articles': articles, 'request': context['request']}


@register.inclusion_tag('staff/staff_element.rss')
def rss_author_element(staffers):
    return {'staffers': staffers}


@register.inclusion_tag('comments/comment_list.rss', takes_context=True)
def rss_comments_items(context, object, comments):
    return {'object': object, 'comments': comments, 'request': context['request']}


@register.inclusion_tag('events/event_list.rss', takes_context=True)
def rss_events_items(context, events):
    return {'events': events, 'request': context['request']}
