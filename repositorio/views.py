import re
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from repositorio.logic.Contacto import Contacto
from repositorio.logic.Documento import Documento
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
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        messages.error(request, 'No puedes acceder a esta pagina publica')
        return redirect('inicioAdminSubadmin')
    else:
        return render(request,'public/inicio.html')
    

def login(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        messages.error(request, 'Usted ya inicio sesión')
        return redirect('inicioAdminSubadmin')
    else:
        if request.method == 'POST':#si recibe algo por post
            form = LoginForm(request.POST)#creame el formulario pasando como argumento los datos del request
            if (form.is_valid()):#si es valido los datos del formulario
                data = request.POST.dict()#usar los datos como un diccionario
                result = Usuarios.login(data)#ejecuta la logica de login y regresa un diccionario de respuesta
                if result['error'] == False and result['usuarioLogeado'] == True:#si la respuesta fue exitosa
                    response = HttpResponseRedirect('/inicioAdminSubadmin')
                    messages.success(request, result['mensaje'])#prepara un mensaje de exito
                    tiempoCookie = (3600 * 24) * 2
                    response.set_cookie('localId', result['localId'], tiempoCookie)
                    return response
                        #return redirect('inicioAdminSubadmin')#Que nos rediriga y nos muestre el mensaje
                        #return redirect('/inicioAdminSubadmin/'+result['mensaje'])
            else:# si hubo error en la respuesta
                    messages.error(request, result['mensaje'])#mandar en la misma pagina el mensaje de error
        else:#si no hay nada en post
            form = LoginForm()#aun asi, iniciame el formulario por si el usuario entra para rellenarlo

    return render(request,'public/login.html', {#que nos redirija a la plantilla donde pertenece esta funcion
        "form": form #mandamos el formulario
    })

def logout(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):#checamos si el usuario se logueo, checando si existe el archivo de datosDeSesion
        Usuarios.eliminarArchivoSesion(nameFile)#si existe, entonces elimina el archivo
        response = HttpResponseRedirect('/login')
        messages.success(request, 'Acaba de cerrar sesión, vuelva pronto!!')#preparamos el mensaje de exito para el redirect
        response.delete_cookie('localId')
        return response
        #return redirect('login')#que me rediriga al login
    else:#raro, pero si entra aqui, entonces el usuario intento cerrar sesion pero nunca se logueo
        return redirect('inicio')#por lo que lo dirigimos a la pagina de index


def inicioAdminSubadmin(request):
    #print(request.COOKIES.get('localId'))
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):#checamos si el usuario se logueo, checando si existe el archivo de datosDeSesion
        ChecarExpiracion.checarSiExpiro(nameFile)#checamos si expiro el token, si es asi dentro de la logica va refrescar el token
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)#obtenemos los datos de sesion del archivo json
        cantidadDeUsuarios = 0 #Iniciamos la variable para poder mandarla
        cantidadDeDocumentos = Documento.contarDocumentos(nameFile)
        if (datosDeSesion['role'] == 'Administrador'):# si es administrador 
            cantidadDeUsuarios = Usuarios.contarUsuarios(nameFile)# entonces cuentame los usuarios
        return render(request,'admin/inicioAdminSubadmin.html', {# redirige a la plantilla donde pertenece esta funcion
            'datosDeSesion': datosDeSesion,# mandamos los datos de sesion para usarlo en la plantilla
            'cantidadDeUsuarios': cantidadDeUsuarios,# mandamos la cantidad de usuarios a la plantilla
            'cantidadDeDocumentos': cantidadDeDocumentos
        })
    else:#si no se logueo
        messages.error(request, 'No tiene permiso para acceder a esta ruta!!')
        return redirect('/')#entonces redirigelo al index

def contacto(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        messages.error(request, 'No puedes acceder a esta pagina publica')
        return redirect('inicioAdminSubadmin')
    else:
        if (request.method == 'POST'):
            form = ContactoForm(request.POST)
            if (form.is_valid()):
                data = request.POST.dict()#usar los datos como un diccionario
                #print(data)
                result = Contacto.crearQuejaySugerencia(data)
                if (result['error'] == False and result['quejaSugerenciaGuardada'] == True):
                    messages.success(request, result['mensaje'])
                    form.clean()
                else:
                    messages.error(request, result['mensaje'])
                #print(result)
        else:
            form = ContactoForm()
        return render(request,'public/contacto.html', {
            'form': form
        })

def registroSub(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        messages.error(request, 'No puedes acceder a esta pagina publica')
        return redirect('inicioAdminSubadmin')
    else: 
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
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if request.method == 'POST':#si recibe algo por post
            form = DocumentoForm(request.POST, request.FILES)#creame el formulario pasando como argumento los datos del request tanto del post como del file
            if (form.is_valid()):#si es valido los datos del formulario
                data = request.POST.dict()#usar los datos como un diccionario
                files = request.FILES
                validarTipoProyecto = Documento.validarTipoProyecto(data, files)
                if (validarTipoProyecto['error'] == True):
                    messages.error(request, validarTipoProyecto['mensaje'])#mandar en la misma pagina el mensaje de error
                #print(data)
                else:
                    #print('todo bien en el view')
                    result = Documento.agregarDocumento(data, files, datosDeSesion['idToken'])
                    if result['error'] == False and result['archivoAgregado'] == True:#si la respuesta fue exitosa
                        messages.success(request, result['mensaje'])#prepara un mensaje de exito
                        return redirect('inicioAdminSubadmin')#Que nos rediriga y nos muestre el mensaje
                        #return redirect('/login/usuarioRegistradoConExito')
                    else:# si hubo error en la respuesta
                        messages.error(request, result['mensaje'])#mandar en la misma pagina el mensaje de error
        else:#si no hay nada en post
            form = DocumentoForm()#aun asi, iniciame el formulario por si el usuario entra para rellenarlo
        return render(request,'admin/agregarDocumentos.html', {
            'datosDeSesion': datosDeSesion,
            'form': form
        })
    else:
        messages.error(request, 'No tiene permisos para acceder a esta ruta')
        return redirect('inicio')

def vistaDocumento(request):
   return render(request,'public/vistaDocumento.html')

def vistaMetadatos(request):
   return render(request,'public/vistaMetadatos.html')

def vistaSubadministradores(request):
    return render(request,'admin/vistaSubadministradores.html')
        
def vistaQuejasSugerencias(request):
<<<<<<< HEAD
    return render(request,'admin/vistaQuejasSugerencias.html')
        

def vistaDocumentosTodos(request):
    return render(request,'admin/vistaDocumentos.html')
=======
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        result = Contacto.getQuejasySugerencias(datosDeSesion['idToken'])
        if (result['error'] == False):
            listaQYS = result['listaQYS']
        else:
            listaQYS = list()
            messages.error(request, result['mensaje'])
        return render(request,'admin/vistaQuejasSugerencias.html', {
            'datosDeSesion': datosDeSesion,
            'listaQYS': listaQYS
        })
    else:
        messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
        return redirect('inicio')
        
>>>>>>> ed71958f36b311624198c118c6cae0e04b25210f
