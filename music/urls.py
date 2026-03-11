from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter


register_converter(FourDigitYearConverter, 'year4')


urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('genres/', views.genres, name='genres_list'),
    path('tracks/', views.TrackListView.as_view(), name='tracks_list'),
    path('tracks/add/', views.TrackCreateView.as_view(), name='track_create'),
    path('tracks/suggest/', views.TrackSuggestionView.as_view(), name='track_suggestion'),
    path('tracks/ping/', views.TrackPingView.as_view(), name='track_ping'),
    path('tracks/demo-orm/', views.tracks_demo_orm, name='tracks_demo'),
    path('tracks/<slug:slug>/edit/', views.TrackUpdateView.as_view(), name='track_update'),
    path('tracks/<slug:slug>/delete/', views.TrackDeleteView.as_view(), name='track_delete'),
    path('tracks/<slug:slug>/', views.TrackDetailView.as_view(), name='track_detail'),
    path('genres/demo-orm/', views.genres_demo_orm, name='genres_demo'),
    path('genres/<int:genre_id>/', views.genre_by_id, name='genre_by_id'),
    path('genres/<slug:genre_slug>/', views.genre_by_slug, name='genre_by_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    path('search/', views.search, name='search'),
    path('add-artist/', views.add_artist, name='add_artist'),
    path('old-genres/', views.old_genres, name='old_genres'),
]
