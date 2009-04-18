import os
from django.conf import settings
import datetime

def get_image_path(instance, filename):
    return get_storage_path(instance, filename, settings.UPLOADED_MEDIA_DIR)

def get_file_path(instance, filename):
    return get_storage_path(instance, filename, 'files')

def get_storage_path(instance, filename, prefix):
    if instance.published_at:
        dt = instance.published_at
    else:
        dt = datetime.date.today()
    return '/'.join([prefix,
                        "%04d" % dt.year,
                        "%02d" % dt.month,
                        "%02d" % dt.day,
                        filename.replace("'",'').replace('"','').replace('\\','').lower()])