import json
from repositorio.logic.atributosFirebase import AF
from django.utils.safestring import mark_safe


class Contacto():

    @staticmethod
    def crearQuejaySugerencia(data):
        result = dict()
        try:
            response = AF.getDataBase().child('quejaSugerencia').push(data)
            if (response['name']):
                result['error'] = False
                result['quejaSugerenciaGuardada'] = True
                result['mensaje'] = 'Se registro con exitó!!'
                return result
            else:
                result['error'] = True
                result['quejaSugerenciaGuardada'] = False
                result['mensaje'] = 'Error al intentar guardar el registro!!'
                return result
        except Exception as e:
            result['error'] = True
            result['quejaSugerenciaGuardada'] = False
            result['mensaje'] = 'No se pudo guardar este registro!!'
            print(e)
            return result

    @staticmethod
    def getQuejasySugerencias(idToken):
        result = dict()
        try:
            all_QuejasySugerencias = AF.getDataBase().child('quejaSugerencia').get(idToken)
            listaQYS = list()
            data = dict()
            for qys in all_QuejasySugerencias.each():
                data = qys.val()
                data['key'] = qys.key()
                listaQYS.append(data)
            result['listaQYS'] = listaQYS
            #print(listaQYS)
            result['error'] = False
            return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'No se obtuvieron las quejas y sugerencias de la base de datos!!'
            print(e)
            return result
    
    @staticmethod
    def eliminarQYS(idToken, key):
        result = dict()
        try:
            response = AF.getDataBase().child("quejaSugerencia").child(key).remove(idToken)
            result['error'] = False
            result['mensaje'] = 'Se elimino con exitó!!'
            return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'No se pudo eliminar el registro!!'
            print(e)
            return result

    @staticmethod
    def contarQYS(nameFile):#este metodo retorna la cantidad de usuarios en la base de datos
        datosDeSesion = Contacto.devolverTodosLosDatosSesion(nameFile)
        qys = AF.getDataBase().child('quejaSugerencia').get(datosDeSesion['idToken']).val()
        if qys == None:
            return 0
        else:
            cantidadDeQYS = len(qys)
            return cantidadDeQYS

    @staticmethod
    def devolverTodosLosDatosSesion(nameFile):#aqui abrimos el json con los datos de session y 
        #lo retornamos para obtener los datos para otros metodos
        with open(nameFile + '.json') as file:
            data = json.load(file)
            return data

