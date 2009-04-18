# Until Django gets their act together, we need to have our own patched copy of this function
# See http://code.djangoproject.com/ticket/10001 & http://code.djangoproject.com/ticket/6271

import re
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy

smart_split_re = re.compile(r'[^\s"\'\\]*("(?:[^"\\]*(?:\\.[^"\\]*)*)"(?=\s|$)'
                            r'|\'(?:[^\'\\]*(?:\\.[^\'\\]*)*)\'(?=\s|$)'
                            r'|[^\s]+)[^\s"\'\\]*')


def smart_split(text):
    r"""
    Generator that splits a string by spaces, leaving quoted phrases together.
    Supports both single and double quotes, and supports escaping quotes with
    backslashes. In the output, strings will keep their initial and trailing
    quote marks.

    >>> list(smart_split(r'This is "a person\'s" test.'))
    [u'This', u'is', u'"a person\\\'s"', u'test.']
    >>> list(smart_split(r"Another 'person\'s' test."))
    [u'Another', u"'person's'", u'test.']
    >>> list(smart_split(r'A "\"funky\" style" test.'))
    [u'A', u'""funky" style"', u'test.']
    >>> list(smart_split(r"A variable='value' should work."))
    [u'A', u"variable='value'", u'should', u'work.']
    >>> list(smart_split(r"A variable='value with spaces' should also work."))
    [u'A', u"variable='value with spaces'", u'should', u'also', u'work.']
    >>> list(smart_split(r'A variable="value with spaces" should also work.'))
    [u'A', u'variable="value with spaces"', u'should', u'also', u'work.']
    >>> list(smart_split(r'A variable="value with spaces and \'escaped quotes\'" should also work.'))
    [u'A', u'variable="value with spaces and \\\'escaped quotes\\\'"', u'should', u'also', u'work.']
    """
    text = force_unicode(text)
    for bit in smart_split_re.finditer(text):
        bit = bit.group(0)
        if bit[0] == '"' and bit[-1] == '"':
            yield '"' + bit[1:-1].replace('\\"', '"').replace('\\\\', '\\') + '"'
        elif bit[0] == "'" and bit[-1] == "'":
            yield "'" + bit[1:-1].replace("\\'", "'").replace("\\\\", "\\") + "'"
        else:
            yield bit
smart_split = allow_lazy(smart_split, unicode)


def split_contents(token):
    split = []
    bits = iter(smart_split(token.contents))
    for bit in bits:
        # Handle translation-marked template pieces
        if bit.startswith('_("') or bit.startswith("_('"):
            sentinal = bit[2] + ')'
            trans_bit = [bit]
            while not bit.endswith(sentinal):
                bit = bits.next()
                trans_bit.append(bit)
            bit = ' '.join(trans_bit)
        split.append(bit)
    return split
