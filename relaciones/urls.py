from . import views
from django.urls import path

app_name = "relaciones"

urlpatterns = [
    path('add-favoritos/<str:anime_id>/', views.agregar_favoritos, name='add-favoritos'),
    path('del-favoritos/<str:anime_id>/', views.eliminar_favoritos, name='del-favoritos'),
    path('add-estados/<str:anime_id>/', views.cambiar_estado, name='add-estado'),
    path('del-estados/<str:anime_id>/', views.eliminar_estado, name='del-estado'),
    path('change-visto/<int:episodio_id>/', views.cambiar_visto, name='change-visto' ),
    path('export-list/', views.exportar_listado, name='export-list'),
    path('import-list/', views.importar_listado, name='import-list'),
]