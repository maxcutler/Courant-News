import os
COURANT_PATH = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# The relative path from your MEDIA_ROOT setting where courant will save
# image files. If your MEDIA_ROOT is set to "/home/justin/media", courant
# will upload your images to "/home/justin/media/photologue".
UPLOADED_MEDIA_DIR = "images"
THUMBNAIL_BASEDIR = "cache"

APPEND_SLASH = False

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'courant.core.caching.middleware.MemcachedMiddleware',
    'courant.core.countthis.middleware.CountThisMiddleware',
    'courant.core.siteconfig.middleware.LoadSettingsMiddleware',
    'courant.core.siteconfig.middleware.ExpireSettingsMiddleware',
    'courant.core.utils.middleware.FileExtensionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'courant.core.mobile.middleware.MobileMiddleware',
    'courant.contrib.shorturls.middleware.ShortUrlMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'courant.core.pages.middleware.TemplatePagesMiddleware',
    'courant.core.maintenancemode.middleware.MaintenanceModeMiddleware',
    'courant.core.utils.middleware.UserBasedExceptionMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'courant.core.media.context_processors.media',
)

AUTH_PROFILE_MODULE = 'news.userprofile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    'django.contrib.redirects',

    'tagging',
    'mptt',
    'comment_utils',
    'sorl.thumbnail',
    'south',
    'pagination',
    'djangosphinx',
    'django_extensions',
    'haystack',
    'chronograph',

    'courant.core.utils',
    'courant.core.utils.captcha',
    'courant.core.gettag',
    #'courant.core.nando', 
    'courant.core.dynamic_models',
    #'courant.core.caching',
    'courant.core.assets',
    'courant.core.staff',
    'courant.core.news',
    'courant.core.contact_form',
    'courant.core.emailthis',
    'courant.core.sharethis',
    'courant.core.countthis',
    'courant.core.events',
    'courant.core.discussions',
    'courant.core.media',
    'courant.core.search',
    'courant.core.registration',
    'courant.core.profiles',
    'courant.core.ads',
    'courant.core.menus',
    #'courant.core.genericadmin',
    'courant.core.pages',
    'courant.core.siteconfig',
    'courant.core.mailer',
)

# Added for Django Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

#FOR RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6LfikwAAAAAAAHZx7-Ly-pzlhJXds_M0-vJqbyys'
RECAPTCHA_PRIVATE_KEY = '6LfikwAAAAAAALeq-cNEAxQIMAlukbqjqZrM2mwb'

AUTH_PROFILE_MODULE = 'profiles.userprofile'
LOGIN_REDIRECT_URL = '/' #If login has no next page to go to, go home

TEMPLATE_TAGS = ('courant.core.utils.templatetags.common_tags',
                 'courant.core.utils.templatetags.common_filters',
                 'courant.core.gettag.templatetags.get',
                 'courant.core.caching.templatetags.smart_cache')

DISPLAY_TYPE_TEMPLATE_FALLBACK = 'default'
