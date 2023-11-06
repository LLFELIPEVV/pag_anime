import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    remember_me = forms.BooleanField(
        label="Recuérdame",
        required=False,  # Esto hace que no sea un campo obligatorio
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

class RegistroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)

        # Itera a través de los campos del formulario y agrega la clase 'form-control' a los widgets
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.PasswordInput, forms.EmailInput, forms.URLInput)):
                field.widget.attrs.update({'class': 'form-control'})
    
    avatar_url = forms.URLField(required=False)
    descripcion_personal = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'pais', 'avatar_url', 'descripcion_personal']
    
    def clean(self):
        cleaned_data = super(RegistroForm, self).clean()
        password = cleaned_data.get('password')
        
        # Verificar si la contraseña contiene consultas SQL maliciosas o palabras prohibidas
        sql_patterns = [
            r'\bSELECT\b',
            r'\bFROM\b',
            r'\bINSERT\b',
            r'\bDELETE\b',
            r'\bUPDATE\b',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, password, re.I):
                self.add_error('password', 'La contraseña no puede contener consultas SQL u palabras prohibidas.')
        
        if len(password) < 8:
            self.add_error('password', 'La contraseña debe tener al menos 8 caracteres.')
        
        return cleaned_data