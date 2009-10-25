
from south.db import db
from django.db import models
from courant.core.headers.models import *

class Migration:
    
    def forwards(self, orm):
        orm.HttpHeader(name="User Agent", header="User-Agent", description="The user agent of the requesting browser. You can use the user agent to detect different types of browsers, such the iPhone or other mobile devices. For more information about user agents, see http://msdn.microsoft.com/en-us/library/ms537503%28VS.85%29.aspx.").save()
        orm.HttpHeader(name="Host", header="Host", description="The host that the browser is requesting. This can be used to filter different subdomains, such as mobile.domain.com.").save()
        orm.HttpHeader(name="Referrer", header="Referer", description="The referring URL that linked the user to your page. This can be used to filter when users arrive from various locations such as Facebook or Twitter. Note that 'referer' is spelled incorrectly as the header.").save()
        
        ua = orm.HttpHeader.objects.get(name="User Agent")
        referer = orm.HttpHeader.objects.get(name="Referrer")
        orm.HeaderRule(name="iPhone", header=ua, domain="", regex="iPhone|iPod", extension_list="iphone html", context_var="iPhone", order="1", enabled=False, admin_override=False).save()
        orm.HeaderRule(name="Mobile (from CakePHP)", header=ua, domain="", regex="(iPhone|MIDP|AvantGo|BlackBerry|J2ME|Opera Mini|DoCoMo|NetFront|Nokia|PalmOS|PalmSource|portalmmm|Plucker|ReqwirelessWeb|SonyEricsson|Symbian|UP\.Browser|Windows CE|Xiino)", extension_list="mobile html", context_var="mobile", order="2", enabled=False, admin_override=False).save()
        orm.HeaderRule(name="Twitter", header=referer, domain="", regex="twitter", extension_list="html", context_var="from_twitter", order="3", enabled=False, admin_override=False).save()

    
    def backwards(self, orm):
        pass
    
    models = {
        'headers.httpheader': {
            'description': ('models.TextField', [], {}),
            'header': ('models.CharField', [], {'max_length': '50'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'})
        },
        'headers.headerrule': {
            'admin_override': ('models.BooleanField', ["'Enable This Rule for Admins for Testing'"], {}),
            'context_var': ('models.CharField', [], {'max_length': '50'}),
            'domain': ('models.CharField', [], {'max_length': '50'}),
            'enabled': ('models.BooleanField', ["'Enable This Rule'"], {}),
            'extension_list': ('models.CharField', [], {'max_length': '50'}),
            'header': ('models.ForeignKey', ["orm['headers.HttpHeader']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'}),
            'order': ('models.PositiveSmallIntegerField', [], {}),
            'regex': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['headers']
