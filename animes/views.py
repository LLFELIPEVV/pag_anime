import json

from animeflv import AnimeFLV
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from .models import Anime

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
    
    return render(request, 'inicio/index.html')