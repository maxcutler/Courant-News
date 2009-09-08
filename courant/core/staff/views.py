from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from courant.core.staff.models import *
from courant.core.utils import render


def staffer_detailed(request, slug):
    staffer = get_object_or_404(Staffer, slug=slug, public_profile=True)
    return render(request, ['staff/custom/%s' % staffer.slug, 'staff/detailed'], {'staffer': staffer})
