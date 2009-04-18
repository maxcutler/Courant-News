from django.conf import settings

from courant.core.utils import captcha


def verify_captcha(sender, comment, request, **kwargs):
    challenge_field = request.POST.get('recaptcha_challenge_field')
    response_field = request.POST.get('recaptcha_response_field')
    client = request.META['REMOTE_ADDR']

    # Don't check recaptcha if the user is logged in.
    if request.user.is_authenticated:
        return True

    check_captcha = captcha.submit(challenge_field, response_field,
                                   settings.RECAPTCHA_PRIVATE_KEY, client)

    return check_captcha.is_valid
