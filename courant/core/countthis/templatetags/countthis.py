from django.template import Library, Node, Variable, VariableDoesNotExist, TemplateSyntaxError
from django.contrib.contenttypes.models import ContentType

from tagging.models import Tag

from courant.core.news.models import Article

from datetime import date, timedelta

register = Library()


class CountThisNode(Node):

    def __init__(self, object, url=None):
        self.object = object
        self.url = url

    def render(self, context):
        object = Variable(self.object).resolve(context)
        if not self.url:
            url = object.get_absolute_url()
        else:
            url = Variable(self.url).resolve(context)

        #Make sure the variable exists so we can add to it
        if not 'countthis' in context['request'].META:
            context['request'].META['countthis'] = []

        #Add the object's path, model name, and id, each object is separated by a ;
        context['request'].META['countthis'].append("%s~%s~%s" % (url, ContentType.objects.get_for_model(object).pk, object.id))

        return ''


def countthis(parser, token):
    """
    Send request to update the count of the object.
    Takes an object and an optional URL. If a URL is not provided, then
    get_absolute_url will be called on the object. If the object does not
    have this function defined, then an error will be thrown.

    Example usage:
        {% countthis object %}
        {% countthis object url %}
    """
    bits = token.contents.split()
    if len(bits) == 2:
        return CountThisNode(bits[1])
    elif len(bits) == 3:
        return CountThisNode(bits[1], bits[2])
    else:
        raise TemplateSyntaxError
countthis = register.tag(countthis)


class MostPopularNode(Node):

    def __init__(self, appmodel, type, limit, days, varname, force=False):
        self.appmodel = appmodel
        self.limit = limit
        self.days = days
        self.varname = varname
        self.force = force

        if type == 'viewed':
            self.type = 'view_count'
        elif type == 'emailed':
            self.type = 'email_count'
        elif type == 'commented':
            self.type = 'comment_count'
        else:
            raise TemplateSyntaxError('The only supported types for this template tag are viewed, emailed, and commented.')

    def render(self, context):
        from courant.core.countthis.models import Statistic
        from datetime import timedelta, datetime

        try:
            self.appmodel = Variable(self.appmodel).resolve(context)
        except VariableDoesNotExist:
            pass #Just leave it alone

        #These are numbers, so either they'll resolve to a variable or resolve will return the number
        self.limit = Variable(self.limit).resolve(context)
        self.days = Variable(self.days).resolve(context)

        #We have to get the ContentType from the app.model string
        appmodel = self.appmodel.split('.')
        content_object = ContentType.objects.get(app_label=appmodel[0], model=appmodel[1])
        content_object_model = content_object.model_class()

        content_type_list = [content_object.pk]
        for related_object in content_object_model._meta.get_all_related_objects():
            if issubclass(related_object.model, content_object_model):
                content_type_list.append(ContentType.objects.get_for_model(related_object.model).pk)

        #Get the right objects
        while True:
            statistics_objects = Statistic.objects.filter(content_type__in=content_type_list, created_at__gte=datetime.now() - timedelta(days=self.days)).order_by('-' + self.type)

            #Do we have enough?
            if self.force and statistics_objects.count() < self.limit:
                self.days = self.days + 7
                continue

            #We have enough!
            statistics_objects = statistics_objects[:self.limit]
            break

        #Create a dictionary of just the content_objects and view_counts, so they don't get Statistic models back and have to do object.content_object
        context[self.varname] = [{appmodel[1]: obj.content_object, 'count': getattr(obj, self.type)} for obj in statistics_objects]
        return ''


def get_bits(bits):
    return {
        'appmodel': bits[2],
        'type': bits[1],
        'limit': bits[-3],
        'days': bits[5],
        'varname': bits[-1],
    }


def get_most_popular(parser, token, force=False):
    """
    Format is get_most_popular viewed/emailed/commented APP.MODEL from last X days limit Y as VARIABLE.
    The day range, limit, and app.model name may be context variables.
    """
    bits = token.contents.split()
    bits = get_bits(bits)
    return MostPopularNode(bits['appmodel'], bits['type'], bits['limit'], bits['days'], bits['varname'])
register.tag('get_most_popular', get_most_popular)


def smart_get_most_popular(parser, token):
    """
    Same format as get_most_popular, but if there aren't enough stories in the days given, it will add seven days and try again.
    """
    bits = token.contents.split()
    bits = get_bits(bits)
    return MostPopularNode(bits['appmodel'], bits['type'], bits['limit'], bits['days'], bits['varname'], force=True)
register.tag('smart_get_most_popular', smart_get_most_popular)


class MostPopularTagsNode(Node):

    def __init__(self, days, limit, varname):
        self.days = int(days)
        self.limit = int(limit)
        self.varname = varname

    def render(self, context):
        first_day = date.today() + timedelta(-self.days)
        articles_in_period = Article.objects.filter(published_at__gte=first_day)
        tags = Tag.objects.usage_for_queryset(articles_in_period, counts=True)
        tags.sort(reverse=True, key=lambda t: t.count)
        context[self.varname] = tags[:self.limit]
        return ''


def get_most_popular_tags(parser, token):
    """
    For the given time period, finds the tags which have been used the most (had the most content tagged with them).

    Example:
        {% get_most_popular_tags from last X days limit Y as VARNAME %}
    """

    bits = token.contents.split()
    if len(bits) != 9:
        raise TemplateSyntaxError, "get_most_popular_tags: invalid parameters"
    return MostPopularTagsNode(bits[3], bits[6], bits[8])
register.tag('get_most_popular_tags', get_most_popular_tags)
