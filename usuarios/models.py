from django.db import models
from django.utils import timezone
from animes.models import length_url
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuariosManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('El campo Email es obligatorio')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Usuarios(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=64)
    fecha_registro = models.DateField(default=timezone.now, null=True)
    pais = models.CharField(max_length=40, null=True)
    avatar_url = models.URLField(max_length=length_url, null=True)
    descripcion_personal = models.CharField(max_length=555, null=True)

    # Lista de campos requeridos
    REQUIRED_FIELDS = ['email', 'password', 'pais']

    # Otros campos personalizables
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UsuariosManager()
