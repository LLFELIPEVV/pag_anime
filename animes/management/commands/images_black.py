import json
import concurrent.futures
import requests

from django.core.management.base import BaseCommand
from PIL import Image
from tqdm import tqdm
from io import BytesIO
from animes.models import Anime

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_image_uniform_color(image_path, target_color):
    img = Image.open(image_path)
    img = img.convert("RGB")
    
    for pixel in img.getdata():
        if pixel != target_color:
            return False
    
    return True

def process_anime(anime, existing_ids):
    image_url = anime.banner_url
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_content = BytesIO(response.content)
            
            # Definir el color objetivo como (#21, #21, #21) en formato RGB
            target_color = hex_to_rgb("#212121")
            
            if is_image_uniform_color(image_content, target_color) and str(anime.id) not in existing_ids:
                return str(anime.id), anime.slug  # Devuelve el ID y el slug del anime
    except Exception as e:
        print(f"Error processing anime {anime.id}: {e}")
        return str(anime.id), anime.slug  # Devuelve el ID y el slug en caso de error
    return None

class Command(BaseCommand):
    help = "Check anime images for uniform color"
    
    def handle(self, *args, **options):
        # Cargar IDs existentes desde el archivo JSON
        existing_ids = {}
        try:
            with open("black_anime_ids.json", "r") as json_file:
                existing_ids = json.load(json_file)
        except FileNotFoundError:
            pass
        
        black_anime_ids = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_anime, anime, existing_ids) for anime in Anime.objects.all()]
            
            # Usamos tqdm para mostrar la barra de progreso sobre los resultados de las tareas completadas
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Procesando animes"):
                result = future.result()
                if result is not None:
                    anime_id, anime_slug = result
                    black_anime_ids[anime_id] = anime_slug

        # Guardar los nuevos IDs de los animes en el archivo JSON en el formato deseado
        with open("black_anime_ids.json", "w") as json_file:
            json.dump(black_anime_ids, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS("IDs de animes con imágenes en negro guardados en black_anime_ids.json"))
