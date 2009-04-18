from django.template import Library, Template, TemplateSyntaxError, Node, Variable

from courant.core.news.models import *
from courant.core.utils.text import split_contents

from datetime import timedelta, datetime

register = Library()

class WeeksIssuesNode(Node):
    def __init__(self, issue, varname):
        self.issue = Variable(issue)
        self.varname = varname
        
    def render(self, context):
        issue = self.issue.resolve(context)
        monday = issue.published_at - timedelta(issue.published_at.weekday())
        days = []
        for i in range(0, 5):
            dt = monday + timedelta(i)
            try:
                i = Issue.objects.get(published_at__year=int(dt.year),
                                                published_at__month=int(dt.month),
                                                published_at__day=int(dt.day))
                days.append({'day': dt, 'issue': i})
            except Issue.DoesNotExist:
                days.append({'day': dt})
        context[self.varname] = days
        return ''   

def do_weeks_issues(parser, token):
    """
    Finds all issues published in the same week as the specified issue.
    
    Syntax::
    
        {% weeks_issues [issue] as [varname ] %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'weeks_issues' tag takes exactly 2 arguments")
    return WeeksIssuesNode(bits[1], bits[3])
register.tag('weeks_issues', do_weeks_issues)