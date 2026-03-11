from django.shortcuts import render

from music.views import MENU


def albums_list(request):
    albums = ['Thriller', 'Back in Black', 'The Dark Side of the Moon', 'Abbey Road']
    context = {
        'title': 'Альбомы каталога',
        'menu': MENU,
        'albums': albums,
    }
    return render(request, 'albums/list.html', context)
