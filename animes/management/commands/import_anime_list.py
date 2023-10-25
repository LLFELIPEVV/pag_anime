import json
import logging
import requests

from tqdm import tqdm
from threading import Lock
from animeflv import AnimeFLV
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from concurrent.futures import ThreadPoolExecutor, wait
from animes.models import Anime, Episodios, Generos, Download_Server, Video_server


genre_lock = Lock()
animes_404 = []

# Define una función para procesar un anime y sus datos relacionados
def process_anime(api, clave, anime_id):
    id_anime = anime_id
    clave_int = int(clave)

    if clave_int % 24 == 0:
        print(f"\nPagina {1 + (clave_int / 24)}\n")

    response = requests.get(f"https://www3.animeflv.net/anime/{id_anime}")

    if response.status_code != 404:
        info_anime = api.get_anime_info(id_anime)
        
        # Tabla Anime
        # Verifica si el anime ya existe en la base de datos
        anime_obj, created = Anime.objects.get_or_create(
            id=id_anime,
            defaults={
                'titulo': info_anime.title,
                'poster_url': info_anime.poster,
                'banner_url': info_anime.banner,
                'sinopsis': info_anime.synopsis,
                'rating': info_anime.rating or "N/A",
                'debut': info_anime.debut,
                'tipo': info_anime.type,
                'orden': clave_int,
            }
        )

        if created:  # El anime es nuevo
            # Tabla Generos

            # Obtén la lista de nombres de géneros desde la fuente externa
            genres_from_source = info_anime.genres

            # Crea una lista para almacenar los objetos Generos a asignar
            genres_to_assign = []

            for genre_name in genres_from_source:
                # Verifica si el género ya existe en la base de datos
                with genre_lock:
                    if not Generos.objects.filter(nombre_genero=genre_name).exists():
                        genre_obj = Generos(nombre_genero=genre_name)
                        genre_obj.save()
                    else:
                        continue

                # Agrega el objeto de género a la lista de géneros a asignar
                genres_to_assign.append(genre_obj)

            # Asigna los géneros al anime
            anime_obj.genero_id.set(genres_to_assign)

            # Tabla Episodios
            episodes = info_anime.episodes
            
            if episodes:
                # Iniciar barra de progreso
                
                with tqdm(total=len(episodes), desc=f"Procesando episodios para {info_anime.title} #{clave_int}") as pbar:
                    existing_episode_numbers = set(Episodios.objects.filter(anime_id=anime_obj).values_list('numero_episodio', flat=True))
                    
                    for episode in episodes:
                        
                        try:
                            
                            if episode.id not in existing_episode_numbers:
                                episodio = Episodios(
                                    anime_id=anime_obj,
                                    numero_episodio=episode.id,
                                    imagen_url_episodio=episode.image_preview
                                )
                                episodio.save()

                                # Tabla Download_Server
                                download_servers_to_create = []

                                download_links = api.get_links(id_anime, episode.id)

                                if download_links:
                                    for link in download_links:
                                        download_server = Download_Server(
                                            episodio_id=episodio,
                                            download_server=link.server,
                                            download_url=link.url
                                        )
                                        download_servers_to_create.append(download_server)

                                # Tabla Video_server
                                video_servers_to_create = []

                                video_servers = api.get_video_servers(id_anime, episode.id)

                                if video_servers:
                                    for server in video_servers[0]:
                                        video_server = Video_server(
                                            episodio_id=episodio,
                                            server=server["server"],
                                            title=server["title"],
                                            ads=server["ads"],
                                            url_episodios=server.get("url", ""),
                                            allow_mobile=server["allow_mobile"],
                                            code=server["code"]
                                        )
                                        video_servers_to_create.append(video_server)

                                # Usamos bulk_create para insertar múltiples registros a la vez
                                Download_Server.objects.bulk_create(download_servers_to_create)
                                Video_server.objects.bulk_create(video_servers_to_create)
                        except IntegrityError as e:
                            # Maneja la excepción de integridad, que ocurre cuando ya existe un episodio con la misma clave única
                            error_msg = f"\nEl episodio con anime ID {id_anime}-{episode.id} ya existía:\n{str(e)}\n"
                        
                        finally:
                            # Actualiza la barra de progreso global para indicar que se ha completado un episodio
                            pbar.update(1)
        else:  # El anime no es nuevo
            episodes = info_anime.episodes

            if episodes:
                # El anime existe, pero puede tener nuevos episodios
                existing_episode_numbers = set(Episodios.objects.filter(anime_id=anime_obj).values_list('numero_episodio', flat=True))
                new_episodes = [episode for episode in episodes if episode.id not in existing_episode_numbers]
                
                if new_episodes:
                    print(f"\nEl anime con ID {id_anime} ya existe en la base de datos, se agregaron nuevos episodios.\n")
                    
                    # Crear una barra de progreso para todos los episodios nuevos
                    with tqdm(total=len(new_episodes), desc=f"Procesando episodios para {info_anime.title} #{clave_int}") as pbar_total:
                        
                        # Iterar a través de los episodios nuevos
                        for episode in new_episodes:
                            try:
                                if episode.id not in existing_episode_numbers:
                                    episodio = Episodios(
                                        anime_id=anime_obj,
                                        numero_episodio=episode.id,
                                        imagen_url_episodio=episode.image_preview
                                    )
                                    episodio.save()

                                    download_servers_to_create = []
                                    video_servers_to_create = []

                                    download_links = api.get_links(id_anime, episode.id)

                                    if download_links:
                                        for link in download_links:
                                            download_server = Download_Server(
                                                episodio_id=episodio,
                                                download_server=link.server,
                                                download_url=link.url
                                            )
                                            download_servers_to_create.append(download_server)

                                    video_servers = api.get_video_servers(id_anime, episode.id)

                                    if video_servers:
                                        for server in video_servers[0]:
                                            video_server = Video_server(
                                                episodio_id=episodio,
                                                server=server["server"],
                                                title=server["title"],
                                                ads=server["ads"],
                                                url_episodios=server.get("url", ""),
                                                allow_mobile=server["allow_mobile"],
                                                code=server["code"]
                                            )
                                            video_servers_to_create.append(video_server)

                                    # No actualices la barra de progreso para el episodio aquí
                            except IntegrityError as e:
                                    # Maneja la excepción de integridad, que ocurre cuando ya existe un episodio con la misma clave única
                                    error_msg = f"\nEl episodio con anime ID {id_anime}-{episode.id} ya existía:\n{str(e)}\n"
                            finally:
                                # Actualiza la barra de progreso global para indicar que se ha completado un episodio
                                pbar_total.update(1)
                else:
                    print(f"\nEl anime con ID {id_anime} ya existe en la base de datos y no tiene nuevos episodios.\n")
    else:
        animes_404.append(id_anime)
        print(f"\nEl anime con ID {id_anime} no se encontró en AnimeFLV (404), se omitió.\n")

class Command(BaseCommand):
    help = 'Importa toda la información de los animes usando los ID de la lista'

    def handle(self, *args, **kwargs):
        global genre_lock, animes_404  # Definir genre_lock y animes_404 como variables globales

        logging.basicConfig(filename='animes_import.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

        api = AnimeFLV()

        with open('lista_id.json') as json_file:
            data = json.load(json_file)

        # Define el rango de claves a procesar
        clave_inicio = 901
        clave_fin = 1100  # Cambia esto para controlar la cantidad de animes que deseas procesar en cada ejecución

        futures = []  # Lista para almacenar los objetos Future

        # Crea un ThreadPoolExecutor para procesar los animes de manera concurrente
        with ThreadPoolExecutor(max_workers=4) as executor:  # Puedes ajustar max_workers según la cantidad de hilos que desees
            for clave, anime in data.items():
                clave_int = int(clave)
                if clave_int >= clave_inicio and clave_int <= clave_fin:
                    # Utiliza executor para procesar los animes en paralelo y almacena los objetos Future
                    future = executor.submit(process_anime, api, clave, anime)
                    futures.append(future)

        # Espera a que todos los hilos terminen
        wait(futures)

        # Cerrar la conexión con la API después de usarla
        api.close()

        # Cerrar el archivo de registro al final de la función handle
        logging.shutdown()
        
        print(animes_404)

        print("Bucle terminado")
