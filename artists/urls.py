from django.urls import path

from . import views


urlpatterns = [
    path('', views.artists_list, name='artists_list'),
]
