from django.conf import settings

def media(request):
    """
    Adds media-related context variables to the context
    
    """
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_MEDIA_URL': settings.STATIC_URL,
        'COURANT_ADMIN_MEDIA_URL': settings.COURANT_ADMIN_MEDIA_URL
    }