#Adapted from http://reviewboard.googlecode.com/svn/trunk/reviewboard/admin/siteconfig.py

from django.conf import settings
from django.contrib.sites.models import Site
from courant.core.siteconfig.models import SiteConfiguration
from courant.core.settings import usersettings


def load_site_config():
    """
    Loads any stored site configuration settings and populates the Django
    settings object with any that need to be there.
    """

    try:
        siteconfig = SiteConfiguration.objects.get_current()
    except SiteConfiguration.DoesNotExist:
        siteconfig = SiteConfiguration(site=Site.objects.get_current(),
                                       version="1.0")
        siteconfig.save()
    except:
        # We got something else. Likely, this doesn't exist yet and we're
        # doing a syncdb or something, so silently ignore.
        return

    #Create defaults dictionary and set them on siteconfig object
    defaults = {}
    for set in usersettings:
        for fieldset in set.values():
            for key, value in fieldset.items():
                defaults[key] = value['default']
    if not siteconfig.get_defaults():
        siteconfig.add_defaults(defaults)

    #Merge the defaults and currently set settings - the current settings will override the defaults
    merged = dict(defaults, **siteconfig.settings)

    for key in merged:
        try:
            getattr(settings, key)
        except AttributeError:
            setattr(settings, key, merged[key])
