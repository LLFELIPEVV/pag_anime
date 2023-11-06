from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.cerrar_sesion, name='logout'),
]