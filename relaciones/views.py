from animes.models import Anime
from .models import usuarios_animes
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# CRUD Favoritos
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
def obtener_favoritos(request):
    user = request.user
    context = []
    favoritos = usuarios_animes.objects.filter(user_id=user, favorito=True).order_by('id', 'fecha_agregado').values_list('anime_id', flat=True)
    
    # Paginación
    paginator = Paginator(favoritos, 24)
    page = request.GET.get('page', 1)
    
    try:
        favoritos_pagina = paginator.page(page)
    except PageNotAnInteger:
        favoritos_pagina = paginator.page(1)
    except EmptyPage:
        favoritos_pagina = paginator.page(paginator.num_pages)
    
    for favorito in favoritos_pagina:
        anime = Anime.objects.get(id=favorito)
        id = favorito
        poster = anime.poster_url
        title = anime.titulo
        type = anime.tipo
        context.append({'title': title, 'type': type,
                        'poster': poster, 'id': id})
    return context

# CRUD Estados
@login_required
def cambiar_estado(request, anime_id):
    if request.method == 'POST':
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
def obtener_estado(request, estado):
    user = request.user
    context = []
    agregados = usuarios_animes.objects.filter(user_id=user, estado=estado).order_by('id', 'fecha_agregado').values_list('anime_id', flat=True)
    
    # Paginación
    paginator = Paginator(agregados, 24)
    page = request.GET.get('page', 1)
    
    try:
        agregados_pagina = paginator.page(page)
    except PageNotAnInteger:
        agregados_pagina = paginator.page(1)
    except EmptyPage:
        agregados_pagina = paginator.page(paginator.num_pages)
    
    for agregado in agregados_pagina:
        anime = Anime.objects.get(id=agregado)
        id = agregado
        poster = anime.poster_url
        title = anime.titulo
        type = anime.tipo
        context.append({'title': title, 'type': type,
                        'poster': poster, 'id': id})
    return context

# Perfil
@login_required
def datos_usuario(request, usuario, anime):
    datos = usuarios_animes.objects.get(user_id=usuario, anime_id=anime)
    return datos
