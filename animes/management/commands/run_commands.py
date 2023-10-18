import os
from django.core.wsgi import get_wsgi_application
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Para usar secuencialmente los módulos que actualizan la información de la base de datos sin tener que entrar en cada uno'

    def handle(self, *args, **kwargs):
        # Cargar el entorno de Django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pagina_anime.settings")
        application = get_wsgi_application()

        # Para actualizar la lista de id
        call_command('list_animes')
        # Para importar los datos de la API de AnimeFLV
        call_command('import_anime_list')
        # Para actualizar la lista de los animes que tienen los banner en negro
        # call_command('images_black')
        # Actualiza la lista de los últimos animes
        call_command('import_last_animes')
        # Actualiza la lista de los últimos episodios
        call_command('import_last_episodes')
