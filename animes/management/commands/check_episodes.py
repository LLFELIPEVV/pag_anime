import json

from tqdm import tqdm
from animeflv import AnimeFLV
from django.core.management.base import BaseCommand
from concurrent.futures import ThreadPoolExecutor, wait
from animes.models import Anime, Generos, Episodios, Video_server, Download_Server

class Command(BaseCommand):
    help = 'Verifica y compara información de anime en la base de datos con la API de AnimeFLV, para saber qué animes tienen su información incompleta'
    
    def __str__(self):
        ejemplo_clase = {
            'mononoke-hime': {
                'Anime': {
                    'titulo': 'Correct', 
                    'sinopsis': 'Correct', 
                    'tipo': 'Correct', 
                    'debut': 'Correct', 
                    'poster_url': 'Correct', 
                    'banner_url': 'Correct', 
                    'rating': 'Correct'
                }, 
                'Generos': [{'accion': 'Incomplete'}, {'aventura': 'Incomplete'}, {'fantasia': 'Incomplete'}], 
                'Episodios': {
                    1: {
                        'estado': 'Correct', 'imagen_url_episodio': 'Correct', 'Video_server': '', 'Download_Server': ''
                    }
                }
            }
        }

        # Devuelve la representación JSON del ejemplo
        return json.dumps(ejemplo_clase, indent=4)

    def handle(self, *args, **options):
        api = AnimeFLV()

        with open('lista_id.json') as json_file:
            data = json.load(json_file)
        
        # Cargar anime_data desde el archivo si existe, para que al reescribir el archivo se mantenga lo que ya venia
        try:
            with open('registro_verificado.json') as existing_data_file:
                anime_data = json.load(existing_data_file)
        except FileNotFoundError:
            anime_data = {}
        
        # Define el rango de claves a procesar
        clave_inicio = 1
        clave_fin = 2  # Cambia esto para controlar la cantidad de animes que deseas procesar en cada ejecución

        futures = []  # Lista para almacenar los objetos Future

        with ThreadPoolExecutor(max_workers=4) as executor:  # Puedes ajustar max_workers según la cantidad de hilos que desees
            for clave, anime in tqdm(data.items(), total=len(data), desc=f"Procesando animes"):
                clave_int = int(clave)
                if clave_inicio <= clave_int <= clave_fin:
                    # Utiliza executor para procesar los animes en paralelo y almacena los objetos Future
                    future = executor.submit(self.process_anime, anime, api, anime_data)
                    futures.append(future)
        
        # Espera a que todos los hilos terminen y recopila los resultados
        for future in tqdm(futures, total=len(futures), desc="Esperando resultados"):
            anime_result = future.result()
            anime_data.update(anime_result)
        
        print("Todos los hilos han terminado.")

        api.close()

        with open('registro_verificado.json', 'w') as json_file:
            json.dump(anime_data, json_file, indent=4)
        print("Proceso finalizado correctamente.")

    def process_anime(self, anime, api, anime_data):
        try:
            anime_obj = Anime.objects.get(id=anime)

            # Crear la estructura de datos si no existe
            anime_result = {
                anime_obj.id: {
                    "Anime": {
                        "titulo": "", "sinopsis": "", "tipo": "", "debut": "", "poster_url": "", "banner_url": "", "rating": ""
                    },
                    "Generos": [],
                    "Episodios": {}
                }
            }
            
            self.check_anime(anime_obj, api, anime_result, anime_data, anime)
            
            return anime_result

        except Anime.DoesNotExist:
            anime_result = {
                anime: {
                    "Anime": {
                        "titulo": "Incomplete", "sinopsis": "Incomplete", "tipo": "Incomplete", "debut": "Incomplete", "poster_url": "Incomplete", "banner_url": "Incomplete", "rating": "Incomplete"
                    },
                    "Generos": ["Incomplete"],
                    "Episodios": {
                        "numero_episodio": "Incomplete",
                        "imagen_url_episodio": "Incomplete"
                    },
                    "Video_server": {
                        "Servers": "Incomplete"
                    },
                    "Download_Server": {
                        "Servers": "Incomplete"
                    }
                }
            }

            return anime_result

    def check_anime(self, anime_obj, api, anime_result, anime_data, anime):
        anime_id = anime_obj.id if anime_obj else anime

        # Obtener la información de la API
        api_info = api.get_anime_info(anime_id)

        # Utilizar la estructura existente si ya hay datos para este anime
        if anime_id not in anime_data:
            anime_data[anime_id] = {
                "Anime": {
                    "titulo": "", "sinopsis": "", "tipo": "", "debut": "", "poster_url": "", "banner_url": "", "rating": ""
                },
                "Generos": [],
                "Episodios": {}
            }

        # Comparar la información del anime en la base de datos con la información de la API
        anime_data[anime_id]["Anime"]["titulo"] = "Correct" if anime_obj.titulo == api_info.title else "Incomplete"
        anime_data[anime_id]["Anime"]["sinopsis"] = "Correct" if anime_obj.sinopsis == api_info.synopsis else "Incomplete"
        anime_data[anime_id]["Anime"]["tipo"] = "Correct" if anime_obj.tipo == api_info.type else "Incomplete"
        anime_data[anime_id]["Anime"]["debut"] = "Correct" if anime_obj.debut == api_info.debut else "Incomplete"
        anime_data[anime_id]["Anime"]["poster_url"] = "Correct" if anime_obj.poster_url == api_info.poster else "Incomplete"
        anime_data[anime_id]["Anime"]["banner_url"] = "Correct" if anime_obj.banner_url == api_info.banner else "Incomplete"
        anime_data[anime_id]["Anime"]["rating"] = "Correct" if str(anime_obj.rating) == api_info.rating else "Incomplete"

        # Verificar información de géneros
        self.check_genero(anime_obj, anime_data, api_info, anime_id)

        # Llama a la función check_episodes usando ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            anime_episodes = list(api_info.episodes)
            for future in tqdm(executor.map(lambda episode: self.check_episodes(anime_obj, api, episode, anime_data, anime_id), anime_episodes),
                            total=len(anime_episodes), desc=f"Procesando episodios de {api_info.title}"):
                pass

    def check_genero(self, anime_obj, anime_data, api_info, anime_id):
        genres = [genre.nombre_genero for genre in anime_obj.genero_id.all()]

        for genre in api_info.genres:
            # Agrega una nueva clave 'Generos' en lugar de sobrescribir
            anime_data[anime_id].setdefault("Generos", []).append({
                f"{genre}": "Correct" if genre in genres else "Incomplete"
            })

    def check_episodes(self, anime_obj, api, episode_api, anime_data, anime_id):
        episode_number = episode_api.id
        episode_imagen = episode_api.image_preview
        episodios = Episodios.objects.filter(anime_id=anime_obj)
        episode_obj = episodios.filter(numero_episodio=episode_number).first()

        anime_data[anime_id]["Episodios"][episode_number] = {
            "estado": "Correct" if episode_obj else "Incomplete",
            "imagen_url_episodio": "Correct" if episode_imagen == episode_obj.imagen_url_episodio else "Incomplete",
            "Video_server": {
                "Servers": {}
            },
            "Download_Server": {
                "Servers": {}
            }
        }

        self.check_video_server(anime_obj, episode_obj, episode_number, api, anime_data, anime_id)
        self.check_download_server(anime_obj, episode_obj, episode_number, api, anime_data, anime_id)

    def check_video_server(self, anime_obj, episode_obj, episode_number, api, anime_data, anime_id):
        video_servers = Video_server.objects.filter(episodio_id=episode_obj)
        video_api = api.get_video_servers(anime_id, episode_number)

        if video_api:
            for server in video_api[0]:
                server_key = server['server']
                server_title = server['title']
                server_ads = server['ads']
                server_url = server.get("url", "")
                server_code = server['code']

                # Utiliza el nombre del servidor como clave en lugar de la estructura de video_api
                if server_key not in anime_data[anime_id]["Episodios"][episode_number]["Video_server"]["Servers"]:
                    anime_data[anime_id]["Episodios"][episode_number]["Video_server"]["Servers"][server_key] = {
                        "server_title": "",
                        "server_ads": "",
                        "server_url": "",
                        "server_code": ""
                    }

                anime_data[anime_id]["Episodios"][episode_number]["Video_server"]["Servers"][server_key] = {
                    "server_title": "Correct" if any(video_server.title == server_title for video_server in video_servers) else "Incomplete",
                    "server_ads": "Correct" if any(video_server.ads == server_ads for video_server in video_servers) else "Incomplete",
                    "server_url": "Correct" if any(video_server.url_episodios == server_url for video_server in video_servers) else "Incomplete",
                    "server_code": "Correct" if any(video_server.code == server_code for video_server in video_servers) else "Incomplete"
                }

    def check_download_server(self, anime_obj, episode_obj, episode_number, api, anime_data, anime_id):
        download_servers = Download_Server.objects.filter(episodio_id=episode_obj)
        download_api = api.get_links(anime_id, episode_number)
        
        anime_data[anime_id]["Episodios"][episode_number].setdefault("Download_Server", {"Servers": {}})

        if download_api:
            for server in download_api:
                server_key = server.server
                server_url = server.url

                anime_data[anime_id]["Episodios"][episode_number]["Download_Server"]["Servers"][server_key] = {
                    "server_key": "Correct" if download_servers.filter(download_server=server_key).exists() else "Incomplete",
                    "server_url": "Correct" if download_servers.filter(download_url=server_url).exists() else "Incomplete"
                }
