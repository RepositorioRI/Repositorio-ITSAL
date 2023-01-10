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
        cantitadTotalDocumentos = Documento.contarDocumentos()
        result = Documento.contarPorCarrera()
        if (result['error'] == False):
            return render(request,'public/inicio.html',{
                'countQuimica': result['countQuimica'],
                'countElectronica': result['countElectronica'],
                'countMecanica': result['countMecanica'],
                'countAcuicultura': result['countAcuicultura'],
                'countIGE': result['countIGE'],
                'countTICS': result['countTICS'],
                'cantitadTotalDocumentos': cantitadTotalDocumentos
            })
        else:
            messages.error(request, result['mensaje'])
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
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            cantidadDeUsuarios = 0 #Iniciamos la variable para poder mandarla
            cantidadDeDocumentos = Documento.contarDocumentos()
            cantidadDeQYS = Contacto.contarQYS(nameFile)
            if (datosDeSesion['role'] == 'Administrador'):# si es administrador 
                cantidadDeUsuarios = Usuarios.contarUsuarios(nameFile)# entonces cuentame los usuarios
            return render(request,'admin/inicioAdminSubadmin.html', {# redirige a la plantilla donde pertenece esta funcion
                'datosDeSesion': datosDeSesion,# mandamos los datos de sesion para usarlo en la plantilla
                'cantidadDeUsuarios': cantidadDeUsuarios,# mandamos la cantidad de usuarios a la plantilla
                'cantidadDeDocumentos': cantidadDeDocumentos,
                'cantidadDeQYS': cantidadDeQYS
            })
        else:
            return redirect('cuentaInhabilitada')
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
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            if request.method == 'POST':#si recibe algo por post
                form = DocumentoForm(request.POST, request.FILES)#creame el formulario pasando como argumento los datos del request tanto del post como del file
                if (form.is_valid()):#si es valido los datos del formulario
                    data = request.POST.dict()#usar los datos como un diccionario
                    files = request.FILES
                    if not Documento.sonIguales(files):
                        validarTipoProyecto = Documento.validarTipoProyecto(data, files)
                        if (validarTipoProyecto['error'] == True):
                            messages.error(request, validarTipoProyecto['mensaje'])#mandar en la misma pagina el mensaje de error
                        #print(data)
                        else:
                            #print('todo bien en el view')
                            result = Documento.agregarDocumento(data, files, datosDeSesion['idToken'])
                            if result['error'] == False and result['archivoAgregado'] == True:#si la respuesta fue exitosa
                                messages.success(request, result['mensaje'])#prepara un mensaje de exito
                                return redirect('vistaDocumentos')#Que nos rediriga y nos muestre el mensaje
                                #return redirect('/login/usuarioRegistradoConExito')
                            else:# si hubo error en la respuesta
                                messages.error(request, result['mensaje'])#mandar en la misma pagina el mensaje de error
                    else:
                        messages.error(request, 'El archivo del proyecto y el archivo de licencia no deben ser iguales!!')#mandar en la misma pagina el mensaje de error
            else:#si no hay nada en post
                form = DocumentoForm()#aun asi, iniciame el formulario por si el usuario entra para rellenarlo
            return render(request,'admin/agregarDocumentos.html', {
                'datosDeSesion': datosDeSesion,
                'form': form
            })
        else:
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos para acceder a esta ruta')
        return redirect('inicio')

def vistaDocumento(request, key):
    print(key)
    if (Documento.esKeyValida(key)):
        result = Documento.getDocumento(key)
        nameFile = request.COOKIES.get('localId')
        if (ChecarExpiracion.seLogueo(nameFile)):
            ChecarExpiracion.checarSiExpiro(nameFile)
            datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
            if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
                if (result['error'] == False):
                    if 'licencia' in result:
                        licencia = result['licencia']
                        linkLicencia = result['linkLicencia']
                    else:
                        licencia = 0
                        linkLicencia = 0
                    return render(request,'public/vistaDocumento.html', {
                        'datosDeSesion': datosDeSesion,
                        'documento': result['documento'],
                        'archivo': result['archivo'],
                        'licencia': licencia,
                        'linkArchivo': result['linkArchivo'],
                        'linkLicencia': linkLicencia,
                        'keyDocumento': result['keyDocumento'],
                        'megabits_redondeados': result['megabits_redondeados']
                    })
                else:
                    messages.error(request, result['mensaje'])
                    return render(request,'public/vistaDocumento.html')
            else:
                return redirect('cuentaInhabilitada')
        else:
            if (result['error'] == False):
                if 'licencia' in result:
                    licencia = result['licencia']
                    linkLicencia = result['linkLicencia']
                else:
                    licencia = 0
                    linkLicencia = 0
                return render(request,'public/vistaDocumento.html', {
                    'documento': result['documento'],
                    'archivo': result['archivo'],
                    'licencia': licencia,
                    'linkArchivo': result['linkArchivo'],
                    'linkLicencia': linkLicencia,
                    'keyDocumento': result['keyDocumento'],
                    'megabits_redondeados': result['megabits_redondeados']
                })
            else:
                messages.error(request, result['mensaje'])
                return render(request,'public/vistaDocumento.html')
    else:
        print('key invalida')
        return redirect('paginaError')

def vistaMetadatos(request, key):
    if (Documento.esKeyValida(key)):
        result = Documento.getDocumento(key)
        nameFile = request.COOKIES.get('localId')
        if (ChecarExpiracion.seLogueo(nameFile)):
            ChecarExpiracion.checarSiExpiro(nameFile)
            datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
            if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
                if (result['error'] == False):
                    if 'licencia' in result:
                        licencia = result['licencia']
                        linkLicencia = result['linkLicencia']
                    else:
                        licencia = 0
                        linkLicencia = 0
                    return render(request,'public/vistaMetadatos.html', {
                        'datosDeSesion': datosDeSesion,
                        'documento': result['documento'],
                        'archivo': result['archivo'],
                        'licencia': licencia,
                        'linkArchivo': result['linkArchivo'],
                        'linkLicencia': linkLicencia,
                        'keyDocumento': result['keyDocumento'],
                        'megabits_redondeados': result['megabits_redondeados']
                    })
                else:
                    messages.error(request, result['mensaje'])
                    return render(request,'public/vistaMetadatos.html')
            else:
                return redirect('cuentaInhabilitada')
        else:
            if (result['error'] == False):
                if 'licencia' in result:
                    licencia = result['licencia']
                    linkLicencia = result['linkLicencia']
                else:
                    licencia = 0
                    linkLicencia = 0
                return render(request,'public/vistaMetadatos.html', {
                    'documento': result['documento'],
                    'archivo': result['archivo'],
                    'licencia': licencia,
                    'linkArchivo': result['linkArchivo'],
                    'linkLicencia': linkLicencia,
                    'keyDocumento': result['keyDocumento'],
                    'megabits_redondeados': result['megabits_redondeados']
                })
            else:
                messages.error(request, result['mensaje'])
                return render(request,'public/vistaMetadatos.html')
    else:
        print('key invalida')
        return redirect('paginaError')

def vistaSubadministradores(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            if (datosDeSesion['role'] == 'Subadministrador'):
                messages.error(request, 'No tiene permisos para acceder a esta ruta')
                return redirect('inicioAdminSubadmin')
            else:
                result = Usuarios.obtenerUsuarios(datosDeSesion['idToken'])
                form = UsuarioEditarForm()
                if (result['error'] == False):
                    listaUsuarios = result['listaUsuarios']
                    if (request.method == 'POST'):
                        form = UsuarioEditarForm(request.POST)
                        if (form.is_valid()):
                            data = request.POST.dict()#usar los datos como un diccionario
                            result2 = Usuarios.editarUsuario(data, datosDeSesion['idToken'])
                            if result2['error'] == False:
                                messages.success(request, result2['mensaje'])
                                result = Usuarios.obtenerUsuarios(datosDeSesion['idToken'])
                                listaUsuarios = result['listaUsuarios']
                            else:
                                messages.error(request, result2['mensaje'])
                            #print(data)
                    #UsuarioEditarForm
                else:
                    listaUsuarios = list()
                    messages.error(request, result['mensaje'])
                return render(request,'admin/vistaSubadministradores.html', {
                    'datosDeSesion': datosDeSesion,
                    'listaUsuarios': listaUsuarios,
                    'form': form
                })
        else:
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos para acceder a esta ruta')
        return redirect('inicio')

        
def vistaQuejasSugerencias(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
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
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
        return redirect('inicio')
        

def vistaDocumentosTodos(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            result = Documento.getDocumentos(datosDeSesion['idToken'])
            if (result['error'] == False):
                listaDocumentos = result['listaDocumentos']
            else:
                listaDocumentos = list()
                messages.error(request, result['mensaje'])
            return render(request,'admin/vistaDocumentos.html', {
                'datosDeSesion': datosDeSesion,
                'listaDocumentos': listaDocumentos
            })
        else:
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
        return redirect('inicio')

def eliminarQYS(request, key):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            result = Contacto.eliminarQYS(datosDeSesion['idToken'], key)
            if (result['error'] == False):
                messages.success(request, result['mensaje'])
            else:
                messages.error(request, result['mensaje'])
            return redirect('vistaQuejasSugerencias')
        else:
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
        return redirect('inicio')

def eliminarUsuario(request, key):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            result = Usuarios.eliminarUsuario(datosDeSesion['idToken'], key)
            if (result['error'] == False):
                messages.success(request, result['mensaje'])
            else:
                messages.error(request, result['mensaje'])
            return redirect('vistaSubadministradores')
        else:
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
        return redirect('inicio')

def cuentaInhabilitada(request):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):#checamos si el usuario se logueo, checando si existe el archivo de datosDeSesion
        Usuarios.eliminarArchivoSesion(nameFile)#si existe, entonces elimina el archivo
        response = HttpResponseRedirect('/login')
        messages.error(request, 'Su cuenta acaba de ser inhabilitada, favor de comunicarse con el administrador!!')#preparamos el mensaje de exito para el redirect
        response.delete_cookie('localId')
        return response
        #return redirect('login')#que me rediriga al login
    else:#raro, pero si entra aqui, entonces el usuario intento cerrar sesion pero nunca se logueo
        return redirect('inicio')#por lo que lo dirigimos a la pagina de index


def vistaDocumentosCarrera(request, career):
    if (Documento.esCarreraValida(career)):
        nameFile = request.COOKIES.get('localId')
        if (ChecarExpiracion.seLogueo(nameFile)):
            messages.error(request, 'No puedes acceder a esta pagina publica')
            return redirect('inicioAdminSubadmin')
        else:
            result = Documento.contarPorCarrera()
            result2 = Documento.getPorCarrera(career)
            cantidadFilas = len(result2['tblCarrera'])
            if (result['error'] == False and result2['error'] == False):
                return render(request,'public/vistaDocumentosCarrera.html',{
                    'countQuimica': result['countQuimica'],
                    'countElectronica': result['countElectronica'],
                    'countMecanica': result['countMecanica'],
                    'countAcuicultura': result['countAcuicultura'],
                    'countIGE': result['countIGE'],
                    'countTICS': result['countTICS'],
                    'tblCarrera': result2['tblCarrera'],
                    'cantidadFilas': cantidadFilas,
                    'career': career
                })
            else:
                if (result['error'] == True and result2['error']):
                    messages.error(request, result['mensaje'] + '\n' + result2['mensaje'])
                elif (result['error'] == True):
                    messages.error(request, result['mensaje'])
                else:
                    messages.error(request, result2['mensaje'])
                return render(request,'public/vistaDocumentosCarrera.html')
    else:
        return redirect('paginaError')

def vistaDocumentosCategorias(request, type):
    if (Documento.esCategoriaValida(type)):
        nameFile = request.COOKIES.get('localId')
        if (ChecarExpiracion.seLogueo(nameFile)):
            messages.error(request, 'No puedes acceder a esta pagina publica')
            return redirect('inicioAdminSubadmin')
        else:
            result = Documento.getPorCategoria(type)
            cantidadFilas = len(result['tblCategoria'])
            if (result['error'] == False):
                return render(request,'public/vistaDocumentosCategorias.html',{
                    'tblCategoria': result['tblCategoria'],
                    'cantidadFilas': cantidadFilas,
                    'type': type
                })
            else:
                messages.error(request, result['mensaje'])
                return render(request,'public/vistaDocumentosCategorias.html')
    else:
        return redirect('paginaError')

def eliminarDocumento(request, key):
    nameFile = request.COOKIES.get('localId')
    if (ChecarExpiracion.seLogueo(nameFile)):
        ChecarExpiracion.checarSiExpiro(nameFile)
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
        if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
            result = Documento.eliminarDocumento(datosDeSesion['idToken'], key)
            if (result['error'] == False):
                messages.success(request, result['mensaje'])
            else:
                messages.error(request, result['mensaje'])
            return redirect('vistaDocumentos')
        else:
            return redirect('cuentaInhabilitada')
    else:
        messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
        return redirect('inicio')

def paginaError(request):
    return render(request, 'public/paginaError.html')

def editarDocumento(request, key):
    if (Documento.esKeyValida(key)):
        nameFile = request.COOKIES.get('localId')
        if (ChecarExpiracion.seLogueo(nameFile)):
            ChecarExpiracion.checarSiExpiro(nameFile)
            datosDeSesion = Usuarios.devolverTodosLosDatosSesion(nameFile)
            if (Usuarios.verificarEstado(nameFile, datosDeSesion['idToken'])):
                #aqui codigo
                result = Documento.getDocumento(key)
                if request.method == 'POST':#si recibe algo por post
                    print(request.FILES)
                    form = EditarDocumentoForm(request.POST, request.FILES)#creame el formulario pasando como argumento los datos del request tanto del post como del file
                    if (form.is_valid()):#si es valido los datos del formulario
                        data = request.POST.dict()#usar los datos como un diccionario
                        files = request.FILES
                        if not Documento.sonIguales2(files, result['documento']):
                            validarTipoProyecto = Documento.validarTipoProyecto2(data, files, result['documento'])
                            if (validarTipoProyecto['error'] == True):
                                messages.error(request, validarTipoProyecto['mensaje'])#mandar en la misma pagina el mensaje de error
                            #print(data)
                            else:
                                result2 = Documento.editarDocumento(data, files, validarTipoProyecto['opcion'], datosDeSesion['idToken'], result['documento'], key)
                                if result2['error'] == False:#si la respuesta fue exitosa
                                    messages.success(request, result2['mensaje'])#prepara un mensaje de exito
                                    return redirect('vistaDocumentos')#Que nos rediriga y nos muestre el mensaje
                                    #return redirect('/login/usuarioRegistradoConExito')
                                else:# si hubo error en la respuesta
                                    messages.error(request, result2['mensaje'])#mandar en la misma pagina el mensaje de error
                        else:
                            messages.error(request, 'El archivo del proyecto y el archivo de licencia no deben ser iguales!!')
                    if (result['error'] == False):
                        if 'licencia' in result:
                            licencia = result['licencia']
                        else:
                            licencia = 0
                        #print(result['documento']['title'])
                        return render(request,'admin/editarDocumento.html', {
                            'datosDeSesion': datosDeSesion,
                            'archivo': result['archivo'],
                            'licencia': licencia,
                            'form': form
                        })
                    else:
                        messages.error(request, result['mensaje'])
                        return render(request,'admin/editarDocumento.html', {
                            'datosDeSesion': datosDeSesion,
                            'form': form
                        })
                else:#si no hay nada en post
                    form = EditarDocumentoForm(initial={
                        'title': result['documento']['title'],
                        'career': result['documento']['career'],
                        'creator': result['documento']['creator'],
                        'contributor': result['documento']['contributor'],
                        'type': result['documento']['type'],
                        'date': result['documento']['date'],
                        'description': result['documento']['description'],
                        'publisher': result['documento']['publisher'],
                        'language': result['documento']['language'],
                        'typeProject': result['documento']['typeProject'],
                        'cc': result['documento']['cc']
                    })#aun asi, iniciame el formulario por si el usuario entra para rellenarlo
                    if (result['error'] == False):
                        if 'licencia' in result:
                            licencia = result['licencia']
                        else:
                            licencia = 0
                        #print(result['documento']['title'])
                        return render(request,'admin/editarDocumento.html', {
                            'datosDeSesion': datosDeSesion,
                            'archivo': result['archivo'],
                            'licencia': licencia,
                            'form': form
                        })
                    else:
                        messages.error(request, result['mensaje'])
                        return render(request,'admin/editarDocumento.html', {
                            'datosDeSesion': datosDeSesion,
                            'form': form
                        })
            else:
                return redirect('cuentaInhabilitada')
        else:
            messages.error(request, 'No tiene permisos de acceder a esta ruta!!')
            return redirect('inicio')  
        #return render(request, 'admin/editarDocumento.html')
    else:
        return redirect('paginaError')
    
def restablecerPassword(request, email):
    #print(email)
    result = Usuarios.restablecerPassword(email)
    if (result['error'] == False):
        messages.success(request, result['mensaje'])
    else:
        messages.error(request, result['mensaje'])
    return redirect('login')