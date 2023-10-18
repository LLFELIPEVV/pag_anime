import traceback #Para mas informacion en los errores

from django.core.management.base import BaseCommand #Para ejecutar como script con permisos en una app de Django
from animeflv import AnimeFLV #Api
from animes.models import Anime, Episodios, Generos, Download_Server, Video_server #Modelos
from concurrent.futures import ThreadPoolExecutor, wait #Procesos multihilo

class Command(BaseCommand):
    help = 'Import anime data from AnimeFLV API, no se usa por que hay varias paginas de id que no se pueden tomar de esta manera, aun asi es la forma en la que se hace sin hacer una json con los id'
    
    #Intentar hacerlo de la ultima pagina a la primera, para poder relacionar mas facil los nuevos capitulos
    def handle(self, *args, **kwargs):
        animes_error = {}
        api = AnimeFLV()
        anime_list = []
        page = 1 #Se cambia para la pagina desde que se va a empezar el bucle
        global pagina
        pagina = []
        while page <= 158:
            animes_on_page = api.list(page)
            if not animes_on_page:
                break
            anime_list.extend(animes_on_page)
            pagina.append(animes_on_page[0].id)
            page += 1
        print(pagina)
        
        def process_anime(anime):
            
            try:
                id_anime = anime.id
                
                if anime.id in pagina:
                    indice = pagina.index(anime.id)
                    print(f"Pagina {158 + indice}") #Se debe cambiar con el page de arriba
                
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
            
            except Exception as e:
                # Handle the 404 error or any other exceptions that occur during the process
                traza_error = traceback.format_exc()
                animes_error[id_anime] = traza_error
                print(f"Error procesando el anime con ID {id_anime}: {str(e)}")
                return None  # Continue with the next anime
        
        # Use ThreadPoolExecutor to run the import_anime_data function in parallel
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_anime, anime) for anime in anime_list]

            # Wait for all futures to complete
            wait(futures)
        
        print(animes_error) #Guardarlo en un archivo
        
        print("Bucle terminado")