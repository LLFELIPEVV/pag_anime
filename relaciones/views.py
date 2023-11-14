from animes.models import Anime
from .models import usuarios_animes
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def agregar_favoritos(request, anime_id):
    if request.method == 'POST':
        user = request.user
        anime = get_object_or_404(Anime, id=anime_id)
        
        relation, created = usuarios_animes.objects.get_or_create(user_id=user, anime_id=anime)
        
        relation.favorito = True
        relation.save()
            
    return redirect(request.META.get('HTTP_REFERER') or 'index')

@login_required
def eliminar_favoritos(request, anime_id):
    if request.method == 'POST':
        user = request.user
        anime = get_object_or_404(Anime, id=anime_id)
        relation = usuarios_animes.objects.get(user_id=user, anime_id=anime)
        relation.favorito = False
        relation.save()
        
    return redirect(request.META.get('HTTP_REFERER') or 'index')

@login_required
def cambiar_estado(request, anime_id):
    if request.method == 'POST':
        print(request.POST)
        user = request.user
        estado = request.POST.get('estado')
        anime = get_object_or_404(Anime, id=anime_id)
        relation, created = usuarios_animes.objects.get_or_create(user_id=user, anime_id=anime)
        relation.estado = estado
        relation.save()
    return redirect(request.META.get('HTTP_REFERER') or 'index')

@login_required
def eliminar_estado(request, anime_id):
    if request.method == 'POST':
        user = request.user
        anime = get_object_or_404(Anime, id=anime_id)
        relation = usuarios_animes.objects.get(user_id=user, anime_id=anime)
        relation.estado = None
        relation.save()
    return redirect(request.META.get('HTTP_REFERER') or 'index')

@login_required
def datos_usuario(request, usuario, anime):
    datos = usuarios_animes.objects.get(user_id=usuario, anime_id=anime)
    return datos