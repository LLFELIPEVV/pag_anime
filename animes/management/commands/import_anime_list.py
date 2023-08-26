import json
import logging
import traceback
import requests
#3775 794 675 594
from django.core.management.base import BaseCommand #Para ejecutar como script con permisos en una app de Django
from animeflv import AnimeFLV #Api
from animes.models import Anime, Episodios, Generos, Download_Server, Video_server #Modelos
from concurrent.futures import ThreadPoolExecutor, wait #Procesos multihilo

class Command(BaseCommand):
    help = 'Importa toda la informacion de los animes usando los ID de la lista'
    
    #Intentar hacerlo de la ultima pagina a la primera, para poder relacionar mas facil los nuevos capitulos
    def handle(self, *args, **kwargs):
        logging.basicConfig(filename='animes_import.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        
        api = AnimeFLV()
        animes_404 = []
        
        with open('lista_id.json') as json_file:
            data = json.load(json_file)
        
        def process_anime(clave, anime): #Toma la clave y valor de el archivo json
            
            try:
                id_anime = anime
                
                if int(clave) % 24 == 0:
                    print(f"Pagina {1 + (int(clave)/24)}")
                
                response = requests.get(f"https://www3.animeflv.net/anime/{id_anime}")
                
                if response.status_code != 404:
                    info_anime = api.get_anime_info(id_anime)
                    
                    # Check if the anime information is not empty
                    if not info_anime:
                        return  # Skip this anime if there's no information
                    
                    # Tabla Anime
                    title = info_anime.title
                    poster = info_anime.poster
                    banner = info_anime.banner
                    synopsis = info_anime.synopsis
                    rating_anim = info_anime.rating
                    debut = info_anime.debut
                    type = info_anime.type

                    # Verifica si el atributo "rating" es None y asigna "N/A" como valor predeterminado
                    if rating_anim is None:
                        rating_anim = "N/A"

                    print(f"Insertando anime con título: {title}")
                        
                    nuevo_anime, _ = Anime.objects.update_or_create(
                        id=id_anime,
                        defaults={
                            'titulo': title,
                            'poster_url': poster,
                            'banner_url': banner,
                            'sinopsis': synopsis,
                            'rating': rating_anim,
                            'debut': debut,
                            'tipo': type,
                        }
                    )

                    # Tabla Generos
                    genres = info_anime.genres
                    for genre in genres:
                        #print(f"Insertando genero con nombre: {genre}")
                        nuevo_genero, _ = Generos.objects.update_or_create(nombre_genero=genre)
                        nuevo_anime.genero_id.add(nuevo_genero)

                    episodes = info_anime.episodes

                    # Tabla Episodios
                    for episode in episodes:
                        episodio_anime = nuevo_anime
                        episode_number = episode.id
                        episode_preview = episode.image_preview
                        
                        if id_anime == "one-piece-tv" or id_anime == "naruto" or id_anime == "naruto-shippuden-hd":
                            print(f"Insertando episodio de {title} con numero: {episode.id}")
                        
                        # Verificar si el episodio ya existe
                        if Episodios.objects.filter(anime_id=episodio_anime, numero_episodio=episode_number).exists():
                            continue  # Saltar la inserción si ya existe
                        
                        nuevo_episodio= Episodios.objects.create(
                                anime_id = episodio_anime,
                                numero_episodio = episode_number,
                                imagen_url_episodio = episode_preview
                        )

                        # Tabla DownloadServer
                        download_links = api.get_links(f"{id_anime}", f"{episode_number}")
                        for link in download_links:
                            download_server = link.server
                            download_url = link.url

                            nuevo_download, _ = Download_Server.objects.update_or_create(
                                episodio_id=nuevo_episodio,
                                download_server=download_server,
                                download_url=download_url
                            )

                        # Tabla Video_server
                        video_servers = api.get_video_servers(f"{id_anime}", f"{episode_number}")
                        if video_servers:
                            for server in video_servers[0]:
                                video_server = server["server"]
                                video_title = server["title"]
                                video_ads = server["ads"]
                                video_url = server.get("url", "")
                                video_allow_mobile = server["allow_mobile"]
                                video_code = server["code"]

                                nuevo_video, _ = Video_server.objects.update_or_create(
                                    episodio_id=nuevo_episodio,
                                    server=video_server,
                                    title=video_title,
                                    ads=video_ads,
                                    url_episodios=video_url,
                                    allow_mobile=video_allow_mobile,
                                    code=video_code
                                )
                else:
                    animes_404.append(id_anime)

            except Exception as e:
                error_msg = f"\nError procesando el anime con ID {id_anime}:\n{str(e)}\n"
                logging.error(error_msg, exc_info=True)
                return None
        
        # Use ThreadPoolExecutor to run the import_anime_data function in parallel
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_anime, clave, anime) for clave, anime in data.items()]
            wait(futures)
            
        print(animes_404)
        
        print("Bucle terminado")
    
if __name__ == '__main__':
    Command().handle()
