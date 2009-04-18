from courant.core.utils import render


def most_popular(request, type='articles', days=7):
    return render(request, ['most_popular/most_popular'], {'type': type, 'days': int(days)})
