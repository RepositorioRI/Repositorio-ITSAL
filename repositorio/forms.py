from django import forms
from django.core import validators
#Aqui se crean los formularios para que django los agregue al html de nuestro sistema
class UsuarioForm(forms.Form):#formulario para la gestion de usuarios
    name = forms.CharField(label='Nombre', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ\u00C0-\u017F ]{3,50}', message="Favor de introducir bien su nombre y no exceder a los 50 caracteres")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    surnames = forms.CharField(label='Apellidos', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ\u00C0-\u017F ]{3,50}', message="Favor de introducir bien su apellido y no exceder a los 50 caracteres")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    email = forms.EmailField(label='Email', max_length=50, required=True, 
        validators=[validators.RegexValidator("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Favor de introducir bien su correo y no exceder a los 50 caracteres")],
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label='Contraseña', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ0-9 ]{6,50}', message="Su contraseña es invalida, no ingresar mas de 50 caracteres")],
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

class LoginForm(forms.Form):#formulario para el login
    email = forms.EmailField(label='Email', max_length=50, required=True, 
        validators=[validators.RegexValidator("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", message="Favor de introducir bien su correo y no exceder a los 50 caracteres")],
        widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label='Contraseña', max_length=50, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ0-9 ]{6,50}', message="Su contraseña es invalida, no ingresar mas de 50 caracteres")],
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

class DocumentoForm(forms.Form):
    #los primeros valores son los que toma el formulario como el value
    IQ = "Ing. Quimica"
    IE = "Ing. Electronica"
    IM = "Ing. Mecanica"
    IA = "Ing. Acuicultura"
    IGE = "Ing. Gestion Empresarial"
    ITICS = "Ing. TIC'S"
    CAREER_CHOICES = [
        #estos valores son los que se muestran y por ende estos no son los que se capturan
        (IQ, "Ing. Quimica"),
        (IE, "Ing. Electronica"),
        (IM, "Ing. Mecanica"),
        (IA, "Ing. Acuicultura"),
        (IGE, "Ing. Gestion Empresarial"),
        (ITICS, "Ing. TIC'S")
    ]

    RR = 'Reporte de residencia'
    T = 'Tesis'
    TYPE_CHOICES = [
        (RR, "Reporte de residencia"),
        (T, "Tesis")
    ]

    E = 'Español'
    I = 'Ingles'
    LANGUAGE_CHOICES = [
        (E, "Español"),
        (I, "Ingles")
    ]

    PI = 'Proyecto interno'
    PE = 'Proyecto externo'
    PROJECT_CHOICES = [
        (PI, "Proyecto interno"),
        (PE, "Proyecto externo")
    ]

    title = forms.CharField(label='Titulo', max_length=100, required=True,
        validators=[validators.RegexValidator('[a-zA-ZÑñ\u00C0-\u017F ]{3,100}', message="Favor de introducir bien el titulo, evite las comas o puntos y texto mayor a 100 caracteres")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Escriba el titulo del documento'}))
    career = forms.ChoiceField(label='Carrera', required=True, choices=CAREER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'}))
    creator = forms.CharField(label='Autor(es)', max_length=250, required=True, 
        validators=[validators.RegexValidator("[a-zA-ZÑñ,\u00C0-\u017F ]{3,250}", message="Favor de introducir bien el o los autores, use las comas en caso de querer anotar a mas autores y no debe exceder de los 250 caracteres")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Escriba el nombre del autor'}))
    contributor = forms.CharField(label='Colaborador(es)', max_length=250, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ,\u00C0-\u017F ]{3,250}', message="Favor de introducir bien el o los asesores, use las comas en caso de querer anotar a mas asesores y no debe exceder de los 250 caracteres")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Escriba nombre del asesor'}))
    type = forms.ChoiceField(label='Tipo de documento', required=True, choices=TYPE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select mb-3'}))
    date = forms.DateField(label='Fecha de publicación', required=True,
        widget=forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date'}, format="%Y-%m-%d"))
    description = forms.CharField(label='Descripción', max_length=1000, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ0-9.,\'\n\u00C0-\u017F ]{20,1000}', message="Favor de introducir bien su descripción, debe tener como minimo 20 caracteres y no debe exceder de los 500 caracteres")],
        widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Escriba la desripcion del documento aquí, favor de evitar acentos', 'style': 'height: 10em;'}))
    publisher = forms.CharField(label='Editor(a)', max_length=100, required=True, 
        validators=[validators.RegexValidator('[a-zA-ZÑñ\u00C0-\u017F ]{3,100}', message="Favor de introducir bien el nombre del editor y no debe de exceder de los 100 caracteres")],
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Escriba el nombre del editor', 'value': 'Instituto Tecnológico de Salina Cruz'}))
    language = forms.ChoiceField(label='Idioma del documento', required=True, choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'}))
    typeProject = forms.ChoiceField(label='Seleccione el tipo de proyecto', required=True, choices=PROJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'}))
    File = forms.FileField(label='Seleccione el documento', required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3', 'accept':'application/pdf'}))
    cc = forms.CharField(label='Ingresa la licencia cc', max_length=500, required=True, 
        validators=[validators.RegexValidator('[a-zA-Z0-9<>:."=/\u00C0-\u017F\- ]{6,500}', message="Su licencia cc es invalida")],
        widget=forms.Textarea(attrs={'class': 'form-control mb-3', 'style': 'height: 6em;'}))
    externalLicense = forms.FileField(label='Seleccione la licencia externa (solo si el proyecto es externo)', required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-3', 'accept':'application/pdf'}))
