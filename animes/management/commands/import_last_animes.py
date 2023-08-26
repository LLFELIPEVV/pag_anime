import json
from animeflv import AnimeFLV
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crear la lista con los id de los animes de los ultimos animes'
    
    def handle(self, *args, **kwargs):
        api = AnimeFLV()
        
        anime_dict = {}  # Inicializar un diccionario vacío
        
        anime_list = api.get_latest_animes()
        
        for anime in anime_list:
            id_episode = anime.id
            banner = anime.banner
            
            # Agregar la entrada del anime al diccionario
            anime_dict[id_episode] = banner
        
        # Imprimir el diccionario para ver si los datos se han recopilado correctamente
        print(anime_dict)
        
        # Guardar el diccionario actualizado en el archivo JSON (reescribir)
        try:
            with open('lista_last_animes.json', 'w') as archivo_json:
                json.dump(anime_dict, archivo_json, indent=4)
            print("Archivo JSON creado exitosamente.")
        except Exception as e:
            print("Error al crear el archivo JSON:", e)


