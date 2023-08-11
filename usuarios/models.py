from django.db import models
from animes.models import length_url

# Create your models here.

class Usuarios(models.Model):
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=64, null=True)
    fecha_registro = models.DateField(null=True)
    pais = models.CharField(max_length=40, null=True)
    avatar_url = models.URLField(max_length=length_url, null=True)
    descripcion_personal = models.CharField(max_length=555, null=True)

