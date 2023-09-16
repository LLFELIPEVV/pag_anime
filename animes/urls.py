from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:query>/', views.anime_search, name='anime_search'),
    path('all/', views.all_animes, name='all_animes'),
    path('listado/', views.listado, name='listado'),
    path('listado/<int:page>/', views.listado, name='listado_pagina'),
    path('search/', views.buscar_animes, name='buscar_animes'),
    path('detalle_anime/<str:anime_id>', views.anime, name='detalle_anime'),
    path('detalle_anime/<str:anime_id>/episodio/<int:episodio>', views.episodio, name='episodio')
]
