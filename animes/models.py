from django.db import models

#Longitudes maximas

length_url = 100

# Create your models here.

class Estados(models.Model):
    nombre_estado = models.CharField(max_length=15, null=True, unique=True)

class Generos(models.Model):
    nombre_genero = models.CharField(max_length=100, null=True, unique=True)
    
    def __str__(self):
        return self.nombre_genero

class Estudios_animacion(models.Model):
    nombre_estudio = models.CharField(max_length=100, null=True)
    fundacion = models.DateField(null=True)
    pais = models.CharField(max_length=100, null=True)

class Anime(models.Model):
    
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG-13'
    R = 'R'
    R18 = 'R18+'
    
    opciones_edad = [
        (G, 'G'),
        (PG, 'PG'),
        (PG_13, 'PG_13'),
        (R, 'R'),
        (R18, 'R18+')
    ]
    
    ANIME = 'Anime'
    PELICULA = 'Película'

    opciones_tipo = [
        (ANIME, 'Anime'),
        (PELICULA, 'Película'),
    ]
    
    id = models.CharField(max_length=255, primary_key=True)
    genero_id = models.ManyToManyField(Generos)
    estudio_id = models.ForeignKey(Estudios_animacion, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=255, null=True, db_collation='utf8mb4_unicode_ci')
    sinopsis = models.TextField(null=True)
    tipo = models.CharField(max_length=50, choices=opciones_tipo, default=ANIME)
    año_lanzamiento = models.DateField(null=True)
    debut = models.CharField(max_length=100, null=True)
    duracion = models.IntegerField(null=True)
    clasificacion_edad = models.CharField(choices=opciones_edad, max_length=6, null=True)
    poster_url = models.URLField(max_length=length_url, null=True)
    banner_url = models.URLField(max_length=length_url, null=True)
    trailer_url = models.URLField(max_length=length_url, null=True)
    total_episodios = models.IntegerField(null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=1)
    
    def __str__(self):
        return self.titulo

class Episodios(models.Model):
    anime_id = models.ForeignKey(Anime, on_delete=models.CASCADE)
    numero_episodio = models.PositiveIntegerField(null=True)
    titulo_episodio = models.CharField(max_length=100, null=True)
    duracion = models.IntegerField(null=True)
    fecha_lanzamiento = models.DateField(null=True)
    sinopsis_episodio = models.TextField(null=True)
    imagen_url_episodio = models.URLField(max_length=length_url, null=True)
    
    def __str__(self):
        return f"{self.anime_id.titulo} - Episodio {self.numero_episodio}"

class Atributos(models.Model):
    anime_id = models.ForeignKey(Anime, on_delete=models.CASCADE)
    nombre_atributo = models.CharField(max_length=100, null=True)
    valor_atributo = models.CharField(max_length=100, null=True)

class Download_Server(models.Model):
    episodio_id = models.ForeignKey(Episodios, on_delete=models.CASCADE)
    download_server = models.CharField(max_length=50)
    download_url = models.URLField()

    def __str__(self):
        return f"{self.download_server} - {self.episodio_id}"

class Video_server(models.Model):
    episodio_id = models.ForeignKey(Episodios, on_delete=models.CASCADE)
    server = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    ads = models.IntegerField(default=0)
    url_episodios = models.URLField(max_length=length_url)
    allow_mobile = models.BooleanField()
    code = models.URLField(max_length=length_url)