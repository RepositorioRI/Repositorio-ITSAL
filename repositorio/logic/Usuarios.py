from repositorio.logic.ChecarExpiracion import ChecarExpiracion
from repositorio.logic.atributosFirebase import *
import json
import os
#la logica por parte de los usuarios
class Usuarios:

    @staticmethod
    def agregarUsaurio(data):#este metodo permite agregar el usuario recibiendo la data
        result = dict()#esta variable es el diccionario que retornamos
        usuario = dict()#esta variable contendra la data que nos interesa subir a la base de datos
        # primero creamos el usuario en autentication
        try:
            auth = AF.getAuth().create_user_with_email_and_password(
                data['email'], data['password'])
            print(auth)
            if auth['localId']:
                try:
                    #una vez creado el usuario en autenticacion de forma exitosa, lo siguiente es crear el usuario en la base de datos
                    #envolvemos la data que nos interesa a la variable que usaremos para subir el usuario a la base de datos
                    usuario['name'] = data['name']
                    usuario['surnames'] = data['surnames']
                    usuario['email'] = data['email']
                    #estos atributos no estan definidos en la data asi que le ponemos un valor
                    usuario['role'] = 'Subadministrador'#el registro son unicamente para los subadministradores
                    usuario['state'] = 'Pendiente'#como ellos mismos se registran, entonces se les coloca como estado pendiente
                    #usamos el metodo set para mandar nuestra propia clave, en este caso es el authID
                    response = AF.getDataBase().child(
                    "usuario").child(auth['localId']).set(usuario, auth['idToken'])#mandamos el token que retorna el registro
                    if response['name']:# si hubo una respuesta
                        result['error'] = False# entonces todo fue un exito
                        result['usuarioAgregado'] = True
                        result['mensaje'] = 'El usuario fue creado con exito, para acceder a su cuenta debe esperar a que el administrador la valide!!'
                        return result# retornamos el result exitoso
                except Exception as e:#si hubo un error al crear el usuario en la base de datos
                    result['error'] = True# entonces que retorne un error
                    result['mensaje'] = 'Ocurrio un error al guardar el usuario en la base de datos'
                    print(repr(e))
                    return result

        except Exception as e:# si hubo un error al crear el usuario en autenticacion
            result['error'] = True# entonces que retorne un error
            result['mensaje'] = 'El email ya es existente por otro usuario'
            print(repr(e))
            return result

    @staticmethod
    def login(data):#este metodo permite realizar el login recibiendo la data
        result = dict()#esta variable es el diccionario que retornamos
        try:
            user = AF.getAuth().sign_in_with_email_and_password(data['email'], data['password'])
            if (user['idToken']):#si hay token significa que se logueo de forma exitosa
                try:#ahora hay que checar si ese usuario existe en la bd y si tambien esta aceptado por el administrador
                    user2 = AF.getDataBase().child('usuario').child(user['localId']).get(user['idToken']).val()
                    if (user2['state'] == 'Pendiente'):#checar si el usuario ya esta aprobado por el administrador
                        result['error'] = True# si no esta aceptado entonces retorna un error
                        result['mensaje'] = 'Esta cuenta aun no esta aprobada por el administrador, favor de intentar mas tarde!!'
                        return result
                    else:# si ya esta aprobado por el administrador
                        #guardamos los datos del logueo
                        datosDeSesion = {
                            'localId': user['localId'],
                            'email': user['email'],
                            'idToken': user['idToken'],
                            'refreshToken': user['refreshToken'],
                            'name': user2['name'],
                            'role': user2['role'],
                            'surnames': user2['surnames']
                        }
                        with open('datosDeSesion.json', 'w') as file:
                            json.dump(datosDeSesion, file)#los datos del logueo los guardamos en un archivo json llamado datosDeSesion
                        ChecarExpiracion.iniciarFechaDeExpiracion()#iniciamos la fecha de expiracion para el token, esto se hacer el otro archivo de logica
                        result['error'] = False#una vez creado el archivo con los datos del logueo, retornamos que todo fue un exito
                        result['usuarioLogeado'] = True
                        result['mensaje'] = 'Bienvenido al reposotiorio ...!!'
                        return result
                except Exception as e:#muy raro, pero si hubo un error al consultar el usuario en la base de datos
                    result['error'] = True#retornamos un error
                    result['mensaje'] = 'Error al obtener el usuario en la base de datos'
                    print(repr(e))
                    return result
            else:# si no hay token
                result['error'] = True#retornamos un error
                result['mensaje'] = 'Error al obtener el token'
                return result
        except Exception as e:#si no encontro el usuario en autenticacion
            result['error'] = True#entonces retornamos un error
            result['mensaje'] = 'El email o contraseña incorrectos'
            print(repr(e))
            return result

    @staticmethod
    def devolverTodosLosDatosSesion():#aqui abrimos el json con los datos de session y 
        #lo retornamos para obtener los datos para otros metodos
        with open('datosDeSesion.json') as file:
            data = json.load(file)
            return data
    
    @staticmethod
    def contarUsuarios():#este metodo retorna la cantidad de usuarios en la base de datos
        datosDeSesion = Usuarios.devolverTodosLosDatosSesion()
        users = AF.getDataBase().child('usuario').get(datosDeSesion['idToken']).val()
        cantidadDeUsuarios = len(users)
        return cantidadDeUsuarios
    
    @staticmethod
    def eliminarArchivoSesion():#este metodo elimina el archivo json con los datos de sesion
        #esto se ejecuta si el usuario cerro sesion
        os.remove('datosDeSesion.json')


    

    
        

