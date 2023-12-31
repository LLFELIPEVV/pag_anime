import json

from animes.models import Anime, Episodios
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import usuarios_animes, vizualicion_episodios_usuario
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

    return {
        'context_favorito': context,
        'paginator_favorito': favoritos_pagina
    }

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
    return {
        'context_estado': context,
        'paginator_estado': agregados_pagina    
    }

# Perfil
@login_required
def datos_usuario(request, usuario, anime):
    datos = usuarios_animes.objects.get(user_id=usuario, anime_id=anime)
    return datos

# CRUD episodios vistos
@login_required
def obtener_episodios_vistos(request, anime_id):
    user = request.user
    anime = get_object_or_404(Anime, id=anime_id)
    
    episodios_vistos = vizualicion_episodios_usuario.objects.filter(user_id=user, episodio_id__anime_id=anime, visto=True).values_list('episodio_id', flat=True)
    
    return episodios_vistos

@login_required
def cambiar_visto(request, episodio_id):
    if request.method == 'POST':
        user = request.user
        episodio = get_object_or_404(Episodios, id=episodio_id)
        
        registro, creado = vizualicion_episodios_usuario.objects.get_or_create(user_id=user, episodio_id=episodio)
        registro = registro if not creado else registro
        
        registro.visto = not registro.visto
        registro.save()
    
    return HttpResponse(status=204)
    
@login_required
def exportar_listado(request):
    user = request.user
    listado = usuarios_animes.objects.filter(user_id=user)
    listado_json = {}
    
    for anime in listado:
        anime_id = str(anime.anime_id.id)
        listado_json[anime_id] = {
            "estado": anime.estado,
            "favorito": anime.favorito,
        }
    
    json_data = json.dumps(listado_json, ensure_ascii=False, indent=2)
    
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="listado_anime.json"'
    
    return response

@login_required
def importar_listado(request):
    if request.method == 'POST' and 'importar' in request.POST:
        try:
            archivo_json = request.FILES['importar']
        
            try:
                with archivo_json.open() as file:
                    contenido_json = file.read().decode('utf-8')
                    listado_importado = json.loads(contenido_json)
                    
                    user = request.user
                    
                    for anime_id, datos_anime in listado_importado.items():
                        anime = get_object_or_404(Anime, id=anime_id)
                        
                        relacion, created = usuarios_animes.objects.get_or_create(user_id=user, anime_id=anime)
                        
                        # Actualiza los campos de la relación
                        relacion.favorito = datos_anime.get('favorito', None)
                        relacion.estado = datos_anime.get('estado', None)
                        relacion.save()

                    return JsonResponse({'mensaje': 'Listado importado exitosamente.'}, status=204)
            except json.JSONDecodeError:
                print('El archivo no es un JSON válido.')
                return HttpResponse(status=204)
            except Exception as e:
                print(f'Error al procesar el archivo: {str(e)} Por favor use un anime_id correcto')
                return HttpResponse(status=204)
        except:
            print("No se proporcionó un archivo para importar.")
            return HttpResponse(status=204)
    