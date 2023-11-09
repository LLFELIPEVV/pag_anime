from . import views
from django.urls import path

app_name = "usuarios"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]
