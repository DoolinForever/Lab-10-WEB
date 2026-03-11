from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter


register_converter(FourDigitYearConverter, 'year4')


urlpatterns = [
    path('', views.index, name='home'),
    path('genres/', views.genres, name='genres_list'),
    path('tracks/', views.tracks_list, name='tracks_list'),
    path('tracks/add/', views.track_create, name='track_create'),
    path('tracks/suggest/', views.track_suggestion, name='track_suggestion'),
    path('tracks/demo-orm/', views.tracks_demo_orm, name='tracks_demo'),
    path('genres/demo-orm/', views.genres_demo_orm, name='genres_demo'),
    path('genres/<int:genre_id>/', views.genre_by_id, name='genre_by_id'),
    path('genres/<slug:genre_slug>/', views.genre_by_slug, name='genre_by_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('search/', views.search, name='search'),
    path('add-artist/', views.add_artist, name='add_artist'),
    path('old-genres/', views.old_genres, name='old_genres'),
]
