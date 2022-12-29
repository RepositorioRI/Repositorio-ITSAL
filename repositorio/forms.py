from django import forms
from django.core import validators
#Aqui se crean los formularios para que django los agregue al html de nuestro sistema
class UsuarioForm(forms.Form):#formulario para la gestion de usuarios
    name = forms.CharField(label='Nombre', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ ]{3,50}', message="Favor de introducir bien su nombre")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    surnames = forms.CharField(label='Apellidos', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ ]{3,50}', message="Favor de introducir bien su apellido")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    email = forms.EmailField(label='Email', max_length=50, required=True, 
        validators=[validators.RegexValidator("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Favor de introducir bien su correo")],
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label='Contraseña', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ0-9 ]{6,50}', message="Su contraseña es invalida")],
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

class LoginForm(forms.Form):#formulario para el login
    email = forms.EmailField(label='Email', max_length=50, required=True, 
        validators=[validators.RegexValidator("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Favor de introducir bien su correo")],
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label='Contraseña', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ0-9 ]{6,50}', message="Su contraseña es invalida")],
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
