from django.contrib import admin
from usuarios.models import Usuarios

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fecha_registro', 'pais', 'avatar_url', 'get_groups', 'is_active', 'is_staff')
    
    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Grupos'
    
    list_filter = ('is_active', 'is_staff')
    
    search_fields = ('username', 'email', 'pais')
    
    readonly_fields = ('descripcion_personal', 'pais')

admin.site.register(Usuarios, UsuariosAdmin)
