import httplib

from django.utils import simplejson

from django.conf import settings
from django.http import HttpResponse

def render_to_json(data, status=httplib.OK):
    return HttpResponse(simplejson.dumps(data),
                        mimetype='application/json',
                        status=status)

def clean_errors(djerrors):
    d={}
    for k, v in djerrors.iteritems():
        d[unicode(k)]=[unicode(x) for x in v]
    return d
    
try:
    get_subject=settings.EMAILTHIS_SUBJECT_GETTER
except AttributeError:
    def get_subject(item):
        return str(item)

