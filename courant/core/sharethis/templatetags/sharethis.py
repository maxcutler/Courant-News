from django.template import Library, Node, Variable
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

from courant.core.sharethis.models import SocialNetwork

register = Library()


class ShareThisNode(Node):

    def __init__(self, name, values, varname):
        self.name, self.values, self.varname = name, values, varname

    def render(self, context):
        code_values = {}
        for key, value in self.values.items():
            code_values[key] = urlencode(Variable(value).resolve(context))

        if code_values['url']:
            code_values['url'] = ''.join(["http://", context['request'].get_host(), code_values['url']])

        returnvalue = {}
        if self.name.lower() == 'all':
            networks = SocialNetwork.objects.filter(enabled=True)
            for network in networks:
                returnvalue[network.name] = mark_safe(network.code % code_values)
        else:
            network = SocialNetwork.objects.get(name__iexact=self.name)
            returnvalue[self.name] = mark_safe(network.code % code_values)

        context[self.varname] = returnvalue
        return ''


def sharethis_display(parser, token):
    bits = token.contents.split()
    if not len(bits) % 2 == 0:
        raise TemplateSyntaxError
    else:
        values = {}
        for i in range(2, len(bits)-2, 2):
            values[bits[i]] = bits[i+1]
        varname = bits[-1]
        return ShareThisNode(bits[1], values, varname)
sharethis_display = register.tag(sharethis_display)
