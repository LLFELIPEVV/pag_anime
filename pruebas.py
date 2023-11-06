from animeflv import AnimeFLV

api = AnimeFLV()
#print(f"info_anime: {api.get_anime_info('under-ninja')}")
#print(f"episodes: {api.get_anime_info('under-ninja').episodes}")
#print(f"genres: {api.get_anime_info('tate-no-yuusha-no-nariagari-season-3').genres}")
#print(f"download_links {api.get_links('under-ninja', 1)}")
print(f"video_servers {api.get_video_servers('the-humanoid', 1)}")

""" print(api.get_video_servers('kodomo-no-omocha', 1))
print(api.get_video_servers('After War Gundam X', 1)) """

#print(f"episodes: {api.get_anime_info('nanatsu-no-taizai').episodes[382]}")
#print(api.list(49))
#anime_list = api.get_latest_animes()
#print(anime_list[0])
#print(anime_list[0].id)
#print(api.get_anime_info('nanatsu-no-taizai'))
#print(api.get_anime_info('akibas-trip-the-animation'))
#print(api.get_anime_info('pokemon-sun-moon'))
#id Anime 2
#title Anime 2
#poster Anime 2
#banner Anime 2
#synopsis Anime 2
#rating Anime 2
#genres Generos 1
#debut Anime 2
#type Anime 2
#episodes #EpisodeInfo(id, anime, image_preview,) [(),(),()] Episodios 3

#print(api.get_links('nanatsu-no-taizai', '1')) [(),(),()]

#server DownloadServer 4
#url DownloadServer 4

#print(api.get_video_servers('nanatsu-no-taizai', '1')) [[{}]]

#for server in servers:
    #print(server)
    #print("////////")
#server 4
#title 4
#ads 4
#url Episodios 4
#allow_mobile 4
#code 4


""" import requests

url = "https://animeflv.net//uploads/animes/banners/962.jpg"
url1 = "https://animeflv.net//uploads/animes/banners/2638.jpg"

try:
    response = requests.head(url1, allow_redirects=True)
    final_url = response.url
    status_code = response.status_code

    if status_code == 200:
        print(f"La imagen en {final_url} está disponible (estado {status_code}).")
    else:
        print(f"La imagen en {final_url} no está disponible (estado {status_code}).")
except requests.ConnectionError:
    print(f"No se pudo conectar a {url1}. Verifique la URL o su conexión a internet.") """

from django.contrib.auth.models import User

# Comprobar si existe un usuario con un nombre de usuario específico
username = 'LFELIPEV'
user_exists = User.objects.filter(username=username).exists()

if user_exists:
    # El usuario existe
    print("El usuario existe en la base de datos.")
else:
    # El usuario no existe
    print("El usuario no existe en la base de datos.")
