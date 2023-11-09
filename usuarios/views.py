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

            messages.success(
                request, 'Usuario creado con éxito. Inicia sesión.', extra_tags='registro')

            return redirect('index')

    else:
        form = RegistroForm()

    return render(request, 'registro/register.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    # Redirige a donde desees después de cerrar la sesión, por ejemplo, a la página de inicio.
    return redirect(request.META.get('HTTP_REFERER', None))


@login_required
def perfil(request):
    user = request.user
    
    if request.method == 'POST':
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

    return render(request, 'perfil/perfil.html', {'user': user})
