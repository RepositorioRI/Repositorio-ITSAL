import datetime
import json
import os

from repositorio.logic.atributosFirebase import AF

class ChecarExpiracion():#la logica por parte del token y expiracion
    
    @staticmethod
    def iniciarFechaDeExpiracion(nameFile):#este metodo sobrescribira el json datosDeSesion para agregar la fecha de expiracion del token
        fechaActual = datetime.datetime.now()# aqui obtenemos la fecha actual
        #timedelta es necesario para tener una variable de la hora que queremos sumar, no se puede hacer de forma directa
        antesDeUnaHora = datetime.timedelta(minutes=55)#55 minutos es menos de la hora, para que se confirme la expiracion
        tiempoDeExpiracion = fechaActual + antesDeUnaHora#aplicamos la suma, recordemos que estos datos son de tipo datetime
        #es por ello que se ocupo timedelta
        data = ChecarExpiracion.devolverTodosLosDatosSesion(nameFile)#aqui obtenemos los datos de la sesion
        tiempoDeExpiracionCadena = tiempoDeExpiracion.strftime("%m/%d/%Y, %H:%M:%S")#pasamos la fecha de expiracion a cadena con un formato para poder agregarlo al json
        
        data['fechaExpiracion'] = ''+tiempoDeExpiracionCadena# lo asignamos a la data para guardarlo en el json
        
        with open(nameFile + '.json', 'w') as file:
            json.dump(data, file)#sobreescribimos el archivo json agregando la fecha de expiracion
    
    @staticmethod
    def seLogueo(nameFile):#este metodo es para checar si existe tanto el cookie como el archivo con los datos de sesion json
        if (nameFile != None and os.path.isfile(nameFile + '.json')):
            return True#si existe la cookie y el archivo que retorne un true
        else:
            return False#si no que retorne un false

    @staticmethod 
    def checarSiExpiro(nameFile):#este metodo es para checar si el token ya expiro
        datosDeSesion = ChecarExpiracion.devolverTodosLosDatosSesion(nameFile)#obtenemos todos los datos de la sesion
        fechaActual = datetime.datetime.now()#obtenemos la fecha actual
        fechaExpiracion = datosDeSesion['fechaExpiracion']#asignamos en una variable la fecha de expiracion que nos devuelve los datos de sesion
        fechaExpiracionDate = datetime.datetime.strptime(fechaExpiracion, '%m/%d/%Y, %H:%M:%S')#lo convertimos en tipo datetime
        if (fechaActual >= fechaExpiracionDate):#comparamos si la fecha actual es mayor o igual a la fecha de expiracion del token
            print('si expiro')
            ChecarExpiracion.refrescarToken(nameFile)#si la fecha actual es mayor o igual significa que ya expiro, entonces refrescamos el token

    @staticmethod
    def refrescarToken(nameFile):#este metodo refrescara el token y modificara el valor del token de los datos de sesion a uno nuevo
        data = ChecarExpiracion.devolverTodosLosDatosSesion(nameFile)#obtenemos los datos de la sesion

        user = AF.getAuth().refresh(data['refreshToken'])#refrescamos el token

        data['idToken'] = user['idToken']#cambiamos al nuevo token
        data['refreshToken'] = user['refreshToken']#cambiamos al nuevo refresh token
        
        with open(nameFile + '.json', 'w') as file:
            json.dump(data, file)#modificamos el archivo de datosDeSesion ahora con un token y refreshToken nuevos

        ChecarExpiracion.iniciarFechaDeExpiracion(nameFile)#LLamamos a este metodo para que actualice la fecha de expiracion


    @staticmethod
    def devolverTodosLosDatosSesion(nameFile):#aqui abrimos el json con los datos de session y 
        #lo retornamos para obtener los datos para otros metodos
        with open(nameFile + '.json') as file:
            data = json.load(file)
            return data
    