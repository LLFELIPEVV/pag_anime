import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .forms import LoginForm, RegistroForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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

    return render(request, 'perfil/perfil.html', {'user': user})
