from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from usuarios.forms import LoginForm, RegistroForm  # Asegúrate de importar el formulario personalizado
from django.contrib.auth import authenticate, login

def login_view(request):
    response_data = {'success': False}  # Establece 'success' como False por defecto

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response_data['success'] = True  # Cambia 'success' a True en caso de éxito
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')
            response_data['error_message'] = 'Credenciales incorrectas'  # Agrega el mensaje de error

    return JsonResponse(response_data)

def register(request):
    form = RegistroForm()
    
    return render(request, 'registro/register.html', {'form': form})
