import json

from animeflv import AnimeFLV
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
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
    with open('lista_id.json') as json_file:
        animes_data = json.load(json_file)
    
    nombres_animes = [animes_data[clave] for clave in animes_data.keys()]
    animes_en_orden = Anime.objects.in_bulk(nombres_animes)
    animes_ordenados = []
    
    for nombre in nombres_animes:
        if nombre in animes_en_orden:
            animes_ordenados.append(animes_en_orden[nombre])
    
    animes_ordenados.reverse()
    
    paginator = Paginator(animes_ordenados, 24)
    page_number = page
    page_obj = paginator.page(page_number)
    
    return render(request, 'listado/listado.html', {'page_obj': page_obj})

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
            poster = f'{Anime.objects.get(id=anime_id).poster_url}'
            title = Anime.objects.get(id=anime_id).titulo
            type = Anime.objects.get(id=anime_id).tipo
            last_dict.append({'title': title, 'type': type, 'poster': poster})
    
    emis_dict = []
    for anime in Anime.objects.filter(debut="En emision"):
        titulo_emision = Anime.objects.get(id=anime.id).titulo
        tipo_emision = Anime.objects.get(id=anime.id).tipo
        emis_dict.append({'title': titulo_emision, 'type': tipo_emision})

    context = {'episodes': episodes_dict, 'last': last_dict, 'emision': emis_dict}  # Combine both dictionaries
    
    return render(request, 'inicio/index.html', context)

