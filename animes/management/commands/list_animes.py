import json

from animeflv import AnimeFLV
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crear la lista con los id de los animes, la lista se usa para importar los animes sin necesidad de recorrerlos directamente desde la pagina debido a que Animeflv tiene paginas que estan dañadas y no dejan importar todo el contenido, asi que de este modo al ejecutar este script lo que hace es actualizar la lista con los nuevos animes'
    
    def handle(self, *args, **kwargs):
        api = AnimeFLV()
        
        # Cargar datos antiguos desde el archivo JSON (si existe)
        try:
            with open('lista_id.json', 'r') as archivo_json:
                anime_dict = json.load(archivo_json)
        except FileNotFoundError:
            # Si el archivo no existe, inicializar un diccionario vacío
            anime_dict = {}
        
        anime_list = []
        page = 150
        while page >= 1:
            # Obtener la lista de animes de la página actual usando la API
            animes_on_page = api.list(page)
            if not animes_on_page:
                # Si no hay más animes en esta página, salir del bucle
                break
            # Agregar los animes de la página a la lista de animes
            
            animes_on_page.reverse() #Invertir la lista para que vaya en el orden de acuerdo
            
            anime_list.extend(animes_on_page)
            # Pasar a la página anterior
            page -= 1
        
        # Obtener el número más alto actual en el diccionario (para continuar agregando)
        # Convertir las claves del diccionario en enteros, obtener el máximo y usarlo como max_number
        max_number = max(map(int, anime_dict.keys()), default=0)
        
        for anime in anime_list:
            id_anime = anime.id
            # Si el id_anime no está en el diccionario, agregarlo con el número adecuado
            if id_anime not in anime_dict.values():
                print(f"Nuevo anime agregado: {id_anime}")
                max_number += 1
                anime_dict[str(max_number)] = id_anime  # Convertir a cadena antes de usar como clave
        
        # Guardar el diccionario actualizado en el archivo JSON
        with open('lista_id.json', 'w') as archivo_json:
            json.dump(anime_dict, archivo_json, indent=4)
        
        print("Lista actualizada")

                