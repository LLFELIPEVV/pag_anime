from django.db import models
from usuarios.models import Usuarios
from animes.models import Anime, Estados, Episodios

# Create your models here.

class usuarios_animes(models.Model):
    user_id = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    anime_id = models.ForeignKey(Anime, on_delete=models.CASCADE)
    estado_id = models.ForeignKey(Estados, on_delete=models.CASCADE)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    fecha_agregado = models.DateField(null=True)
    comentario = models.CharField(max_length=100)

class vizualicion_episodios_usuario(models.Model):
    user_id = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    episodio_id = models.ForeignKey(Episodios, on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)