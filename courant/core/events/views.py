from datetime import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from courant.core.events.models import *
from courant.core.utils import render


def event_archive(request, year=None, month=None, day=None):
    kwargs = {}

    if year:
        kwargs['date__year'] = int(year)
    if month:
        kwargs['date__month'] = int(month)
    if day:
        kwargs['date__day'] = int(day)

    events = Event.objects.filter(**kwargs).order_by('-date')

    #Paginate
    paginator = Paginator(events, 35, 5)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        events_paginated = paginator.page(page)
    except (EmptyPage, InvalidPage):
        events_paginated = paginator.page(paginator.num_pages)

    return render(request, ['events/archive'], {'events': events_paginated})


def event_detailed(request, slug, year, month, day):
    kwargs = {'slug': slug,
              'date': datetime.datetime(int(year), int(month), int(day))}
    event = Event.objects.get(**kwargs)
    return render(request, ['events/detailed'], {'event': event})


def event_submit(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            # do something.
    else:
        form = EventForm()
    return render(request, ["events/submit"], {"form": form})
