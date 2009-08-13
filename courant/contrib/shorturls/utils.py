from django.conf import settings

VALID = settings.SHORTURLS_VALID_CHARS or 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def gen_shortcut(num):
    """
    Generates a short URL for any URL on your Django site.  It is intended to
    make long URLs short, a la TinyURL.com.

    Thanks to Jonathan Geddes for the help with this one.
    """
    short = ''
    while num != 0:
        num, remainder = divmod(num - 1, len(VALID))
        short += VALID[remainder]
    return short