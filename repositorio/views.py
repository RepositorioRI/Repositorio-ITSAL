from django.shortcuts import redirect, render
from django.http import HttpResponse
#importamos la clase que contiene los atributos del firebase
from repositorio.logic.atributosFirebase import *
#importamos la logica de usuarios
from repositorio.logic.Usuarios import *
#libreria para los formularios
from repositorio.forms import *
#libreria para mensajes en redirect y render
from django.contrib import messages

# Create your views here.

def inicio(request):
    if (ChecarExpiracion.seLogueo()):
        messages.error(request, 'No puedes acceder a esta pagina publica')
        return redirect('inicioAdminSubadmin')
    else:
        return render(request,'public/inicio.html')
    

def login(request):
    if (ChecarExpiracion.seLogueo()):
        messages.error(request, 'Usted ya inicio sesión')
        return redirect('inicioAdminSubadmin')
    else:
        if request.method == 'POST':#si recibe algo por post
            form = LoginForm(request.POST)#creame el formulario pasando como argumento los datos del request
            if (form.is_valid()):#si es valido los datos del formulario
                data = request.POST.dict()#usar los datos como un diccionario
                result = Usuarios.login(data)#ejecuta la logica de login y regresa un diccionario de respuesta
                if result['error'] == False and result['usuarioLogeado'] == True:#si la respuesta fue exitosa
                    messages.success(request, result['mensaje'])#prepara un mensaje de exito
                    return redirect('inicioAdminSubadmin')#Que nos rediriga y nos muestre el mensaje
                    #return redirect('/inicioAdminSubadmin/'+result['mensaje'])
                else:# si hubo error en la respuesta
                    messages.error(request, result['mensaje'])#mandar en la misma pagina el mensaje de error
        else:#si no hay nada en post
            form = LoginForm()#aun asi, iniciame el formulario por si el usuario entra para rellenarlo

    return render(request,'public/login.html', {#que nos redirija a la plantilla donde pertenece esta funcion
        "form": form #mandamos el formulario
    })

def logout(request):
    if (ChecarExpiracion.seLogueo()):#checamos si el usuario se logueo, checando si existe el archivo de datosDeSesion
        Usuarios.eliminarArchivoSesion()#si existe, entonces elimina el archivo
        messages.success(request, 'Acaba de cerrar sesión, vuelva pronto!!')#preparamos el mensaje de exito para el redirect
        return redirect('login')#que me rediriga al login
    else:#raro, pero si entra aqui, entonces el usuario intento cerrar sesion pero nunca se logueo
        return redirect('inicio')#por lo que lo dirigimos a la pagina de index


def inicioAdminSubadmin(request):
    if (ChecarExpiracion.seLogueo()):#checamos si el usuario se logueo, checando si existe el archivo de datosDeSesion
        ChecarExpiracion.checarSiExpiro()#checamos si expiro el token, si es asi dentro de la logica va refrescar el token
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion()#obtenemos los datos de sesion del archivo json
        cantidadDeUsuarios = 0 #Iniciamos la variable para poder mandarla
        if (datosDeSesion['role'] == 'Administrador'):# si es administrador 
            cantidadDeUsuarios = Usuarios.contarUsuarios()# entonces cuentame los usuarios
        return render(request,'admin/inicioAdminSubadmin.html', {# redirige a la plantilla donde pertenece esta funcion
            'datosDeSesion': datosDeSesion,# mandamos los datos de sesion para usarlo en la plantilla
            'cantidadDeUsuarios': cantidadDeUsuarios# mandamos la cantidad de usuarios a la plantilla
        })
    else:#si no se logueo
        return redirect('/')#entonces redirigelo al index

def contacto(request):
    if (ChecarExpiracion.seLogueo()):
        messages.error(request, 'No puedes acceder a esta pagina publica')
        return redirect('inicioAdminSubadmin')
    else:
        return render(request,'public/contacto.html')

def registroSub(request):
    if request.method == 'POST':#si recibe algo por post
        form = UsuarioForm(request.POST)#creame el formulario pasando como argumento los datos del request
        if (form.is_valid()):#si es valido los datos del formulario
            data = request.POST.dict()#usar los datos como un diccionario
            result = Usuarios.agregarUsaurio(data)#ejecuta la logica de registro y regresa un diccionario de respuesta
            if result['error'] == False and result['usuarioAgregado'] == True:#si la respuesta fue exitosa
                messages.success(request, result['mensaje'])#prepara un mensaje de exito
                return redirect('login')#Que nos rediriga y nos muestre el mensaje
                #return redirect('/login/usuarioRegistradoConExito')
            else:# si hubo error en la respuesta
                messages.error(request, result['mensaje'])#mandar en la misma pagina el mensaje de error
    else:#si no hay nada en post
        form = UsuarioForm()#aun asi, iniciame el formulario por si el usuario entra para rellenarlo
    return render(request,'public/registroSub.html', {#que nos redirija a la plantilla donde pertenece esta funcion
        "form": form #mandamos el formulario
        })

def agregarDocumentos(request):
    if (ChecarExpiracion.seLogueo()):
        ChecarExpiracion.checarSiExpiro()
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion()
        return render(request,'admin/agregarDocumentos.html', {
            'datosDeSesion': datosDeSesion
        })
    else:
        messages.error(request, 'No tiene permisos para acceder a esta ruta')
        return redirect('inicio')

def vistaDocumento(request):
   return render(request,'public/vistaDocumento.html')

def vistaMetadatos(request):
   return render(request,'public/vistaMetadatos.html')
        