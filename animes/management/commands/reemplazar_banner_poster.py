import json
from django.core.management.base import BaseCommand
from animes.models import Anime  # Reemplaza 'tu_app' con el nombre de tu aplicación

class Command(BaseCommand):
    help = 'Actualiza el campo banner_url de los animes en base a un archivo JSON'

    def handle(self, *args, **options):
        # Nombre del archivo JSON que contiene los títulos de los animes a actualizar
        json_file = 'black_anime_ids.json'

        try:
            with open(json_file) as file:
                titles_to_update = json.load(file)
                for key, value in titles_to_update.items():
                    try:
                        anime = Anime.objects.get(id=value)
                        # Obtener la URL del poster
                        poster_url = anime.poster_url
                        # Reemplazar "covers" con "banners" en la URL
                        banner_url = poster_url.replace("/covers/", "/banners/")
                        # Actualiza el campo banner_url
                        anime.banner_url = banner_url
                        anime.save()
                        self.stdout.write(self.style.SUCCESS(f'Se actualizó el anime: {value}'))
                    except Anime.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'No se encontró el anime: {value}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'El archivo JSON {json_file} no se encontró.'))

