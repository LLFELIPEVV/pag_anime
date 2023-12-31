import json

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, RegistroForm
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from relaciones.views import obtener_favoritos, obtener_estado, agregar_favoritos, cambiar_estado, eliminar_favoritos, eliminar_estado

def login_view(request):
    response_data = {'success': False, 'error_message': None}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = request.POST.get('remember_me')
            user = authenticate(request, username=username, password=password)

            if user:
                if remember_me:
                    # Configura un tiempo de vencimiento largo para la sesión
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                login(request, user)
                response_data['success'] = True
            else:
                response_data['error_message'] = 'Credenciales incorrectas'

            return JsonResponse(response_data)


def register(request):
    if request.method == 'POST':
        # Recibe los datos enviados por el usuario
        form = RegistroForm(request.POST)

        if form.is_valid():
            # commit=false es para permitir mas acciones o comprobaciones antes de guardar en la base de datos de otro modo se podria guardar solo con form.save()
            usuario = form.save(commit=False)
            password = form.cleaned_data['password']
            usuario.set_password(password)
            usuario.save()
            
            print(usuario)
            print(password)

            messages.success(
                request, 'Usuario creado con éxito. Inicia sesión.', extra_tags='registro')

            return redirect('index')

    else:
        form = RegistroForm()

    return render(request, 'registro/register.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    # Redirige a donde desees después de cerrar la sesión, por ejemplo, a la página de inicio.
    return redirect(request.META.get('HTTP_REFERER') or 'index')

@login_required
def perfil(request):
    user = request.user
    
    #Favoritos
    favoritos_data = obtener_favoritos(request)
    context_favorito = favoritos_data['context_favorito']
    paginator_favorito = favoritos_data['paginator_favorito']
    #Estados
    abandonado_data = obtener_estado(request, 'Abandonados')
    context_abandonado = abandonado_data['context_estado']
    paginator_abandonado = abandonado_data['paginator_estado']
    completado_data = obtener_estado(request, 'Completados')
    context_completado = completado_data['context_estado']
    paginator_completado = completado_data['paginator_estado']
    espera_data = obtener_estado(request, 'En Espera')
    context_espera = espera_data['context_estado']
    paginator_espera = espera_data['paginator_estado']
    planeado_data = obtener_estado(request, 'Planeados')
    context_planeado = planeado_data['context_estado']
    paginator_planeado = planeado_data['paginator_estado']
    proceso_data = obtener_estado(request, 'En Proceso')
    context_proceso = proceso_data['context_estado']
    paginator_proceso = proceso_data['paginator_estado']
    
    #Formulario
    if request.method == 'POST':
        if 'form-datos-perfil' in request.POST:
            # Actualizar los campos del usuario con los datos del formulario
            user.email = request.POST.get('email', user.email)
            user.pais = request.POST.get('pais', user.pais)
            user.descripcion_personal = request.POST.get('descripcion_personal', user.descripcion_personal)
            
            # Si se ha cargado una nueva imagen, actualizar el avatar
            if 'avatar_url' in request.FILES:
                if user.avatar_url:
                    default_storage.delete(user.avatar_url.name)
                    
                user.avatar_url = request.FILES['avatar_url']

            # Contraseña
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            
            if new_password and new_password == confirm_new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
            elif new_password and new_password != confirm_new_password:
                messages.error(request, "Las contraseñas no coinciden. Inténtalo de nuevo.")
            
            # Guardar los cambios en la base de datos
            user.save()

            # Redirigir a la página de perfil u otra página de confirmación
            return redirect('usuarios:perfil')
        
        elif 'form-estados' in request.POST:
            estado = request.POST.get('estado')
            estado_inicial = request.POST.get('estado_inicial')
            animes_id = request.POST.getlist('selected_animes')
            
            if estado == 'Favoritos':
                for id in animes_id:
                    agregar_favoritos(request, id)
            elif estado == 'Eliminar':
                if estado_inicial == 'Favoritos':
                    for id in animes_id:
                        eliminar_favoritos(request, id)
                else:
                    for id in animes_id:
                        eliminar_estado(request, id)
            else:
                try:
                    for id in animes_id:
                        cambiar_estado(request, id)
                except Exception as e:
                    print(f"El error al cambiar el estado '{estado}' fue: {e}")
            return redirect('usuarios:perfil')

    return render(request, 'perfil/perfil.html', {'user': user, 'context_favorito': context_favorito, 'paginator_favorito': paginator_favorito, 'context_abandonado': context_abandonado, 'paginator_abandonado': paginator_abandonado, 'context_completado': context_completado, 'paginator_completado': paginator_completado, 'context_espera': context_espera, 'paginator_espera': paginator_espera, 'context_planeado': context_planeado, 'paginator_planeado': paginator_planeado, 'context_proceso': context_proceso, 'paginator_proceso': paginator_proceso})
