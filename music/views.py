from django.contrib import messages
from django.db.models import Avg, CharField, Count, ExpressionWrapper, F, FloatField, Q, Sum, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import TrackForm, TrackSuggestionForm
from .models import Genre, GenreAudience, Track

MENU = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Жанры', 'url_name': 'genres_list'},
    {'title': 'Треки', 'url_name': 'tracks_list'},
    {'title': 'Добавить трек', 'url_name': 'track_create'},
    {'title': 'Предложить трек', 'url_name': 'track_suggestion'},
    {'title': 'Артисты', 'url_name': 'artists_list'},
    {'title': 'Альбомы', 'url_name': 'albums_list'},
    {'title': 'Поиск', 'url_name': 'search'},
    {'title': 'Добавить артиста', 'url_name': 'add_artist'},
]

SECTIONS = [
    {
        'title': 'Жанры',
        'description': 'Собраны популярные стили и направления музыки.',
        'url_name': 'genres_list',
    },
    {
        'title': 'Артисты',
        'description': 'Имена исполнителей для быстрого знакомства.',
        'url_name': 'artists_list',
    },
    {
        'title': 'Альбомы',
        'description': 'Классические релизы, с которых удобно начинать прослушивание.',
        'url_name': 'albums_list',
    },
    {
        'title': 'Поиск',
        'description': 'Простой поиск по любому ключевому слову.',
        'url_name': 'search',
    },
    {
        'title': 'Добавить артиста',
        'description': 'Форма для заявки на нового музыканта.',
        'url_name': 'add_artist',
    },
]


def index(request):
    context = {
        'title': 'Музыкальный каталог',
        'menu': MENU,
        'description': 'Добро пожаловать в демо-каталог музыки. Выберите раздел, чтобы продолжить.',
        'sections': SECTIONS,
    }
    return render(request, 'music/index.html', context)


def genres(request):
    genres_context = Genre.published.order_by('name')
    context = {
        'title': 'Жанры каталога',
        'menu': MENU,
        'genres': genres_context,
    }
    return render(request, 'music/genres.html', context)


def genre_by_id(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    return HttpResponse(
        f'<h1>Жанр по id</h1>'
        f'<p>Вы выбрали жанр: {genre.name}</p>'
    )


def genre_by_slug(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    return HttpResponse(
        f'<h1>Жанр по слагу</h1>'
        f'<p>Вы выбрали жанр: {genre.name}</p>'
    )


def tracks_list(request):
    tracks = (
        Track.objects.select_related('genre')
        .prefetch_related('tags')
        .filter(is_published=True)
        .order_by('-release_year', 'title')
    )
    context = {
        'title': 'Треки каталога',
        'menu': MENU,
        'tracks': tracks,
    }
    return render(request, 'music/tracks.html', context)


def track_create(request):
    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save()
            messages.success(request, f'Трек «{track.title}» успешно добавлен.')
            return redirect('tracks_list')
        messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = TrackForm()
    context = {
        'title': 'Добавить трек',
        'menu': MENU,
        'form': form,
    }
    return render(request, 'music/track_form.html', context)


def track_suggestion(request):
    form = TrackSuggestionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            messages.success(request, 'Спасибо! Мы изучим вашу идею и добавим трек позже.')
            form = TrackSuggestionForm()
        else:
            messages.error(request, 'Проверьте введённые данные.')
    context = {
        'title': 'Предложить трек',
        'menu': MENU,
        'form': form,
    }
    return render(request, 'music/track_suggestion.html', context)


def tracks_demo_orm(request):
    q_queryset = (
        Track.objects.select_related('genre')
        .filter(
            Q(is_published=True),
            Q(duration__gte=300) | Q(tags__slug='live'),
        )
        .distinct()
    )

    q_results = q_queryset.values('title', 'genre__name', 'duration')

    base_genre = Genre.objects.first()
    f_result = None
    if base_genre:
        temp_track, _ = Track.objects.get_or_create(
            slug='demo-track-temp',
            defaults={
                'title': 'Demo Track Temp',
                'duration': 180,
                'release_year': 2026,
                'play_count': 0,
                'is_published': False,
                'genre': base_genre,
            },
        )
        Track.objects.filter(pk=temp_track.pk).update(play_count=F('play_count') + 1)
        temp_track.refresh_from_db()
        f_result = {'title': temp_track.title, 'play_count': temp_track.play_count}
        temp_track.delete()

    value_samples = (
        Track.objects.annotate(source_label=Value('Каталог', output_field=CharField()))
        .values('title', 'source_label')
        [:3]
    )

    tag_counts = (
        Track.objects.annotate(tag_total=Count('tags'))
        .values('title', 'tag_total')
        .order_by('-tag_total', 'title')
    )

    track_stats = Track.objects.aggregate(
        total_duration=Sum('duration'),
        avg_duration=Avg('duration'),
    )

    genre_groups = (
        Track.objects.values('genre__name')
        .annotate(track_count=Count('id'))
        .order_by('-track_count')
    )

    duration_minutes = (
        Track.objects.annotate(
            duration_minutes=ExpressionWrapper(
                F('duration') / Value(60.0),
                output_field=FloatField(),
            )
        )
        .values('title', 'duration', 'duration_minutes')
        [:3]
    )

    context = {
        'title': 'Демо ORM по трекам',
        'menu': MENU,
        'q_results': q_results,
        'f_result': f_result,
        'value_samples': value_samples,
        'tag_counts': tag_counts,
        'track_stats': track_stats,
        'genre_groups': genre_groups,
        'duration_minutes': duration_minutes,
    }
    return render(request, 'music/tracks_demo.html', context)


def genres_demo_orm(request):
    output = []

    all_genres = Genre.objects.all()
    output.append(f'Всего жанров в базе: {all_genres.count()}')

    temp_genre = Genre.objects.create(
        name='Demo Genre',
        slug='demo-genre',
        audience=GenreAudience.KIDS,
        is_published=False,
    )
    output.append(f'Создан жанр: {temp_genre}')

    temp_genre.is_published = True
    temp_genre.save(update_fields=['is_published'])
    output.append('Жанр обновлен: установлен is_published=True')

    adults_genres = Genre.objects.filter(audience=GenreAudience.ADULTS).order_by('-created_at')
    output.append(f'Жанры для взрослых (по дате ↓): {[genre.name for genre in adults_genres]}')

    temp_genre.delete()
    output.append('Демо-жанр удален')

    return HttpResponse('<br>'.join(output))


def archive(request, year):
    return HttpResponse(f'<h1>Архив по годам</h1><p>Год: {year}</p>')


def search(request):
    query = request.GET.get('q', '').strip()
    context = {
        'title': 'Поиск по каталогу',
        'menu': MENU,
        'query': query,
    }
    if query:
        context['message'] = f'Результаты поиска по запросу: {query}'
    else:
        context['message'] = 'Вы не задали поисковый запрос.'
    return render(request, 'music/search.html', context)


def add_artist(request):
    success_message = None
    submitted_name = ''
    if request.method == 'POST':
        submitted_name = request.POST.get('name', '').strip()
        if submitted_name:
            success_message = f'Исполнитель {submitted_name} успешно добавлен (демо).'
    context = {
        'title': 'Добавить исполнителя',
        'menu': MENU,
        'success_message': success_message,
        'submitted_name': submitted_name,
    }
    return render(request, 'music/add_artist.html', context)


def old_genres(request):
    genres_url = reverse('genres_list')
    return redirect(genres_url)
