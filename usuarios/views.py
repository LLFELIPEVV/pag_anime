from django.http import JsonResponse
from usuarios.forms import LoginForm  # Asegúrate de importar el formulario personalizado
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Credenciales incorrectas'})
    
    # Manejo de errores o cualquier otro caso
    return JsonResponse({'success': False, 'message': 'Error en la solicitud'})


