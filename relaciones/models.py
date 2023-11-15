from django.db import models
from usuarios.models import Usuarios
from animes.models import Anime, Estados, Episodios
from django.utils import timezone

# Create your models here.

class usuarios_animes(models.Model):
    opciones_estado = [
    ('planeados', 'Planeados'),
    ('proceso', 'En Proceso'),
    ('completados', 'Completados'),
    ('abandonados', 'Abandonados'),
    ('espera', 'En Espera'),
    ]
    
    user_id = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    anime_id = models.ForeignKey(Anime, on_delete=models.CASCADE)
    favorito = models.BooleanField(default=False)
    estado = models.CharField(max_length=50, choices=opciones_estado, null=True, blank=True)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    fecha_agregado = models.DateField(default=timezone.now)
    comentario = models.TextField(null=True, blank=True)

class vizualicion_episodios_usuario(models.Model):
    user_id = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    episodio_id = models.ForeignKey(Episodios, on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)