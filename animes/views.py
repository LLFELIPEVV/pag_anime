import json
import requests
import random

from animeflv import AnimeFLV
from django.shortcuts import render
from usuarios.forms import LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Anime, Episodios, Video_server, Download_Server

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
    orden = request.GET.get('orden', '-orden')  # Si 'orden' no está presente, usa 'orden' como valor predeterminado
    if orden == 'titulo':
        anime_queryset = anime_queryset.order_by('titulo')
    elif orden == 'rating':
        anime_queryset = anime_queryset.order_by('-rating')  # El '-' indica orden descendente
    elif orden == 'default':
        anime_queryset = anime_queryset.order_by('-orden')

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
    
    form = LoginForm()

    return render(request, 'listado/listado.html', {'page_obj': page_obj, 'orden': orden, 'tipo': tipo, 'debut': debut, 'form': form})

def index(request):
    with open('lista_episodes.json') as json_file:
        episodes_data = json.load(json_file)

        episodes_dict = []
        
        for anime_id, anime_info in episodes_data.items():
            episode_number = anime_info['id_episode']
            imagen = str(anime_info['imagen'])
            titulo = Anime.objects.get(id=anime_id).titulo
            numero = int(episode_number)
            
            episodes_dict.append({'id': anime_id,'titulo': titulo, 'poster': imagen, 'numero': numero})
    
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

    random_animes = []
    for anime in random.sample(list(Anime.objects.all()), 6):
        if requests.get(anime.banner_url) != '404':
            random_animes.append(anime)

    form = LoginForm()
    
    context = {'episodes': episodes_dict, 'last': last_dict, 'emision': emis_dict, 'random': random_animes, 'form': form}  # Combine both dictionaries
    
    
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
        
    form = LoginForm()

    return render(request, 'listado/busqueda.html', {'resultados': busqueda_obj, 'query': query, 'page': page_actual, 'form': form})

def anime(request, anime_id):
    anime = Anime.objects.get(id=anime_id)
    id = anime.id
    titulo = anime.titulo
    tipo = anime.tipo
    poster = anime.poster_url
    banner = anime.banner_url
    debut = anime.debut
    sinopsis = anime.sinopsis
    generos = anime.genero_id.all()
    rating = anime.rating
    episodios = Episodios.objects.filter(anime_id=anime_id)
    
    form = LoginForm()
    
    datos = []
    datos.append({'id': id, 'titulo': titulo, 'tipo':tipo, 'poster': poster, 'banner': banner, 'debut': debut, 'sinopsis': sinopsis, 'generos': generos, 'rating': rating, 'episodios': episodios})
    
    return render(request, 'detalle_anime/anime.html', {'datos': datos, 'form': form})

def episodio(request, anime_id, episodio):
    try:
        # Convierte 'episodio' a un valor decimal (float) si es necesario
        episodio = float(episodio)

        # Obtiene el ID del anime y otros datos necesarios
        id = Anime.objects.get(id=anime_id).id
        anime = Anime.objects.get(id=anime_id)
        titulo = anime.titulo
        id_episodio = Episodios.objects.get(anime_id_id=anime_id, numero_episodio=episodio).id
        servidores = Video_server.objects.filter(episodio_id=id_episodio)
        episodios = Episodios.objects.filter(anime_id=anime_id)
        enlace = Download_Server.objects.filter(episodio_id_id=id_episodio)

        # Si 'episodio' es un número entero, conviértelo a entero y elimina los ceros decimales
        if episodio.is_integer():
            episodio = int(episodio)

        form = LoginForm()
        
        datos = [{'id': id, 'titulo': titulo, 'episodio': episodio, 'servidores': servidores, 'episodios': episodios, 'enlace': enlace}]
    
        return render(request, 'episodios/episodio.html', {'datos': datos, 'form':form})
    except ValueError:
        pass
