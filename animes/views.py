import io
import json
import random
import requests
import threading

from PIL import Image, UnidentifiedImageError
from usuarios.views import login_view
from animeflv import AnimeFLV
from django.shortcuts import render
from usuarios.forms import LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Anime, Episodios, Video_server, Download_Server
from relaciones.views import datos_usuario

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
    # Define response_data con un valor predeterminado
    response_data = {'success': False}
    form = LoginForm()
    error_message = None

    if request.method == 'POST':
        response_data = login_view(request)  # Llama a la vista de usuarios
        response_data_json = json.loads(response_data.content)

        print(response_data_json['error_message'])

        if response_data_json['success'] == True:
            error_message = "Inicio de sesión realizado con éxito"
        else:
            error_message = response_data_json['error_message']

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
    # Si 'orden' no está presente, usa 'orden' como valor predeterminado
    orden = request.GET.get('orden', '-orden')
    if orden == 'titulo':
        anime_queryset = anime_queryset.order_by('titulo')
    elif orden == 'rating':
        anime_queryset = anime_queryset.order_by(
            '-rating')  # El '-' indica orden descendente
    elif orden == 'default':
        anime_queryset = anime_queryset.order_by('-orden')

    # Procesar la consulta paginada como antes
    last_dict = []
    for anime in anime_queryset:
        id = anime.id
        poster = anime.poster_url
        title = anime.titulo
        type = anime.tipo
        last_dict.append({'title': title, 'type': type,
                         'poster': poster, 'id': id})

    paginator = Paginator(last_dict, 24)
    page_number = page
    page_obj = paginator.page(page_number)

    # Obtener los filtros seleccionados
    tipo = "&tipo=" + "&tipo=".join(tipos) if tipos else ""
    debut = "&debut=" + "&debut=".join(estados) if estados else ""

    form = LoginForm()

    return render(request, 'listado/listado.html', {'page_obj': page_obj, 'orden': orden, 'tipo': tipo, 'debut': debut, 'form': form, 'error': error_message})

# Definir una función que maneje una solicitud HTTP


def fetch_image(anime, result):
    response = requests.get(anime.banner_url)
    if response.status_code == 200:
        try:
            # Intenta abrir la respuesta como una imagen
            img = Image.open(io.BytesIO(response.content))
            # Si no hay excepciones, consideramos que es una imagen válida
            result.append(anime)
        except (IOError, UnidentifiedImageError) as e:
            # Si se lanza una excepción al abrir la imagen, la respuesta no contiene una imagen válida
            print(
                f"Error al abrir la imagen para el anime {anime.titulo}: {e}")


def index(request):
    if hasattr(request, 'user') and request.user.is_authenticated:
        # Una sesión está abierta y el usuario está autenticado
        usuario_actual = request.user
        print(f"Usuario conectado: {usuario_actual}")
    elif hasattr(request, 'user') and not request.user.is_authenticated:
        print("Una sesión está abierta, pero el usuario no está autenticado")
        # Esto podría ser un usuario anónimo o una sesión no autenticada
    else:
        print("No hay una sesión abierta en absoluto")

    # Define response_data con un valor predeterminado
    response_data = {'success': False}
    form = LoginForm()
    error_message = None

    if request.method == 'POST':
        response_data = login_view(request)  # Llama a la vista de usuarios
        response_data_json = json.loads(response_data.content)

        print(response_data_json['error_message'])

        if response_data_json['success'] == True:
            error_message = "Inicio de sesión realizado con éxito"
        else:
            error_message = response_data_json['error_message']

    with open('lista_episodes.json') as json_file:
        episodes_data = json.load(json_file)

        episodes_dict = []

        for anime_id, anime_info in episodes_data.items():
            episode_number = anime_info['id_episode']
            imagen = str(anime_info['imagen'])
            titulo = Anime.objects.get(id=anime_id).titulo
            numero = int(episode_number)

            episodes_dict.append(
                {'id': anime_id, 'titulo': titulo, 'poster': imagen, 'numero': numero})

    with open('lista_last_animes.json') as json_file:
        last_data = json.load(json_file)

        last_dict = []

        for anime_id, anime_info in last_data.items():
            id = Anime.objects.get(id=anime_id).id
            poster = f'{Anime.objects.get(id=anime_id).poster_url}'
            title = Anime.objects.get(id=anime_id).titulo
            type = Anime.objects.get(id=anime_id).tipo
            last_dict.append({'title': title, 'type': type,
                             'poster': poster, 'id': id})

    emis_dict = []
    for anime in Anime.objects.filter(debut="En emision"):
        id = Anime.objects.get(id=anime.id).id
        titulo_emision = Anime.objects.get(id=anime.id).titulo
        tipo_emision = Anime.objects.get(id=anime.id).tipo
        emis_dict.append(
            {'title': titulo_emision, 'type': tipo_emision, 'id': id})

    random_animes = []
    selected_animes = random.sample(list(Anime.objects.all()), 6)

    result = []  # Lista para almacenar los resultados de las solicitudes HTTP

    # Crear hilos para manejar las solicitudes HTTP
    threads = [threading.Thread(target=fetch_image, args=(
        anime, result)) for anime in selected_animes]

    # Iniciar los hilos
    for thread in threads:
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    random_animes = result  # Utiliza los resultados obtenidos en los hilos

    context = {'episodes': episodes_dict, 'last': last_dict, 'emision': emis_dict,
               'random': random_animes, 'form': form, 'error': error_message}  # Combine both dictionaries

    return render(request, 'inicio/index.html', context)


def buscar_animes(request):
    # Define response_data con un valor predeterminado
    response_data = {'success': False}
    form = LoginForm()
    error_message = None

    if request.method == 'POST':
        response_data = login_view(request)  # Llama a la vista de usuarios
        response_data_json = json.loads(response_data.content)

        print(response_data_json['error_message'])

        if response_data_json['success'] == True:
            error_message = "Inicio de sesión realizado con éxito"
        else:
            error_message = response_data_json['error_message']

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
        busqueda.append({'title': title, 'type': type,
                        'poster': poster, 'id': id})

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

    return render(request, 'listado/busqueda.html', {'resultados': busqueda_obj, 'query': query, 'page': page_actual, 'form': form, 'error': error_message})


def anime(request, anime_id):
    # Define response_data con un valor predeterminado
    response_data = {'success': False}
    form = LoginForm()
    error_message = None

    if request.method == 'POST':
        response_data = login_view(request)  # Llama a la vista de usuarios
        response_data_json = json.loads(response_data.content)

        print(response_data_json['error_message'])

        if response_data_json['success'] == True:
            error_message = "Inicio de sesión realizado con éxito"
        else:
            error_message = response_data_json['error_message']

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

    #Formulario
    form = LoginForm()
    
    #Datos usuario
    relacion = False
    try:
        usuario = request.user.id
        relacion = datos_usuario(request, usuario, id)
    except:
        print("No existen los datos de este usuario")

    datos = []
    datos.append({'id': id, 'titulo': titulo, 'tipo': tipo, 'poster': poster, 'banner': banner,
                 'debut': debut, 'sinopsis': sinopsis, 'generos': generos, 'rating': rating, 'episodios': episodios})

    return render(request, 'detalle_anime/anime.html', {'datos': datos, 'form': form, 'error': error_message, 'relacion': relacion})


def episodio(request, anime_id, episodio):
    # Define response_data con un valor predeterminado
    response_data = {'success': False}
    form = LoginForm()
    error_message = None

    if request.method == 'POST':
        response_data = login_view(request)  # Llama a la vista de usuarios
        response_data_json = json.loads(response_data.content)

        print(response_data_json['error_message'])

        if response_data_json['success'] == True:
            error_message = "Inicio de sesión realizado con éxito"
        else:
            error_message = response_data_json['error_message']

    try:
        # Convierte 'episodio' a un valor decimal (float) si es necesario
        episodio = float(episodio)

        # Obtiene el ID del anime y otros datos necesarios
        id = Anime.objects.get(id=anime_id).id
        anime = Anime.objects.get(id=anime_id)
        titulo = anime.titulo
        id_episodio = Episodios.objects.get(
            anime_id_id=anime_id, numero_episodio=episodio).id
        servidores = Video_server.objects.filter(episodio_id=id_episodio)
        episodios = Episodios.objects.filter(anime_id=anime_id)
        enlace = Download_Server.objects.filter(episodio_id_id=id_episodio)

        # Si 'episodio' es un número entero, conviértelo a entero y elimina los ceros decimales
        if episodio.is_integer():
            episodio = int(episodio)

        form = LoginForm()

        datos = [{'id': id, 'titulo': titulo, 'episodio': episodio,
                  'servidores': servidores, 'episodios': episodios, 'enlace': enlace}]

        return render(request, 'episodios/episodio.html', {'datos': datos, 'form': form, 'error': error_message})
    except ValueError:
        pass
