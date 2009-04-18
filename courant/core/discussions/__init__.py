from django.contrib.comments.signals import comment_will_be_posted
from courant.core.utils.captcha.functions import verify_captcha

comment_will_be_posted.connect(verify_captcha)
