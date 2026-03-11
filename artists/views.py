from django.shortcuts import render

from music.views import MENU


def artists_list(request):
    artists = ['Queen', 'Metallica', 'ABBA', 'Muse', 'Muse']
    context = {
        'title': 'Артисты каталога',
        'menu': MENU,
        'artists': artists,
    }
    return render(request, 'artists/list.html', context)
