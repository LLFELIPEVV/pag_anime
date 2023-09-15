import json
import requests
import random

from animeflv import AnimeFLV
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Anime, Episodios

# Create your views here.

def anime_search(request, query):
    # Crea una instancia de la API de AnimeFLV
    api = AnimeFLV()

    # Realiza una búsqueda basada en el query recibido
    search_results = api.search(query)

    # Renderiza el template y envía los resultados de la búsqueda al contexto
    return render(request, 'search_results.html', {'results': search_results})

def all_animes(request):
    # Crear una instancia del objeto AnimeFLV
    api = AnimeFLV()

    # Obtener una lista completa de todos los animes
    all_animes_info = []
    page = 1
    while True:
        animes_on_page = api.list(page)
        if not animes_on_page:
            break
        all_animes_info.extend(animes_on_page)
        page += 1

    # Renderizar el template y pasar la información de los animes como contexto
    return render(request, 'all_animes.html', {'animes': all_animes_info})

def listado(request, page=1):
    # Obtén todos los animes de la base de datos
    anime_queryset = Anime.objects.all()

    # Filtrar por tipo (Anime, Película, OVA)
    tipos = request.GET.getlist('tipo')
    if tipos:
        anime_queryset = anime_queryset.filter(tipo__in=tipos)

    # Filtrar por estado (En emisión, Finalizado, Próximamente)
    estados = request.GET.getlist('debut')
    if estados:
        anime_queryset = anime_queryset.filter(debut__in=estados)

    # Obtener el valor del parámetro 'orden' y establecer un valor predeterminado si no está presente
    orden = request.GET.get('orden')
    if orden == 'titulo':
        anime_queryset = anime_queryset.order_by('titulo')
    elif orden == 'rating':
        anime_queryset = anime_queryset.order_by('-rating')  # El '-' indica orden descendente

    # Procesar la consulta paginada como antes
    last_dict = []
    for anime in anime_queryset:
        id = anime.id
        poster = anime.poster_url
        title = anime.titulo
        type = anime.tipo
        last_dict.append({'title': title, 'type': type, 'poster': poster, 'id': id})

    paginator = Paginator(last_dict, 24)
    page_number = page
    page_obj = paginator.page(page_number)

    # Obtener los filtros seleccionados
    tipo = "&tipo=" + "&tipo=".join(tipos) if tipos else ""
    debut = "&debut=" + "&debut=".join(estados) if estados else ""

    return render(request, 'listado/listado.html', {'page_obj': page_obj, 'orden': orden, 'tipo': tipo, 'debut': debut})




def index(request):
    with open('lista_episodes.json') as json_file:
        episodes_data = json.load(json_file)

        episodes_dict = []
        
        for anime_id, anime_info in episodes_data.items():
            episode_number = anime_info['id_episode']
            imagen = str(anime_info['imagen'])
            titulo = Anime.objects.get(id=anime_id).titulo
            numero = int(episode_number)
            episodes_dict.append({'titulo': titulo, 'poster': imagen, 'numero': numero})
    
    with open('lista_last_animes.json') as json_file:
        last_data = json.load(json_file)
        
        last_dict = []
        
        for anime_id, anime_info in last_data.items():
            id = Anime.objects.get(id=anime_id).id
            poster = f'{Anime.objects.get(id=anime_id).poster_url}'
            title = Anime.objects.get(id=anime_id).titulo
            type = Anime.objects.get(id=anime_id).tipo
            last_dict.append({'title': title, 'type': type, 'poster': poster, 'id': id})
    
    emis_dict = []
    for anime in Anime.objects.filter(debut="En emision"):
        id = Anime.objects.get(id=anime.id).id
        titulo_emision = Anime.objects.get(id=anime.id).titulo
        tipo_emision = Anime.objects.get(id=anime.id).tipo
        emis_dict.append({'title': titulo_emision, 'type': tipo_emision, 'id': id})

    random_animes = random.sample(list(Anime.objects.all()), 6)
    
    context = {'episodes': episodes_dict, 'last': last_dict, 'emision': emis_dict, 'random': random_animes}  # Combine both dictionaries
    
    return render(request, 'inicio/index.html', context)

def buscar_animes(request):
    query = request.GET.get('q')
    resultados = []  # Inicializa resultados como una lista vacía
    busqueda = []  # Inicializa busqueda como una lista vacía

    # Comprueba si 'query' tiene un valor antes de realizar la consulta en la base de datos
    if query is not None:
        resultados = Anime.objects.filter(titulo__icontains=query)

    # Formatea los resultados si los hay
    for anime in resultados:
        id = anime.id
        poster = anime.poster_url
        title = anime.titulo
        type = anime.tipo
        busqueda.append({'title': title, 'type': type, 'poster': poster, 'id': id})
    
    """ print(resultados)
    print(busqueda)
    print(query) """
    
    page = request.GET.get('page')
    page_actual = 1  # Valor predeterminado para la página actual

    # Verifica si 'page' es un número entero válido
    if page:
        try:
            page_actual = int(page)
        except ValueError:
            page_actual = 1

    paginator = Paginator(busqueda, 24)

    try:
        busqueda_obj = paginator.page(page_actual)
    except PageNotAnInteger:
        # Si la página no es un número entero válido, muestra la primera página
        busqueda_obj = paginator.page(1)
    except EmptyPage:
        # Si la página está vacía, muestra la última página
        busqueda_obj = paginator.page(paginator.num_pages)

    return render(request, 'listado/busqueda.html', {'resultados': busqueda_obj, 'query': query, 'page': page_actual})

def anime(request, anime_id):
    anime = Anime.objects.get(id=anime_id)
    titulo = anime.titulo
    tipo = anime.tipo
    poster = anime.poster_url
    banner = anime.banner_url
    debut = anime.debut
    sinopsis = anime.sinopsis
    generos = anime.genero_id.all()
    rating = anime.rating
    episodios = Episodios.objects.filter(anime_id=anime_id)
    
    datos = []
    datos.append({'titulo': titulo, 'tipo':tipo, 'poster': poster, 'banner': banner, 'debut': debut, 'sinopsis': sinopsis, 'generos': generos, 'rating': rating, 'episodios': episodios})
    
    print(datos)
    
    return render(request, 'detalle_anime/anime.html', {'datos': datos})