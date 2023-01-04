
import json
from repositorio.logic.atributosFirebase import AF


class Documento:

    @staticmethod
    def agregarDocumento(data, files, idToken):
        result = dict()
        response3 = dict()#estas variables las inicializamos porque puede ser que el usuario mande la licencia externa y puede que no la mande
        response5 = dict()
        try:
            response = AF.getDataBase().child("proyecto").push(data, idToken)
            if response['name']:
                try:
                    dataArchivo = dict()
                    dataLicencia = dict()
                    response2 = AF.getStorage().child("pdf/" + response['name'] + "/" + files['File'].name).put(files['File'], idToken)
                    if ('externalLicense' in files):
                        response3 = AF.getStorage().child("pdf/" + response['name'] + "/" + files['externalLicense'].name).put(files['externalLicense'], idToken)
                    else:
                        response3['name'] = True #Si no hay nada para externalLicense entonces le asignamos true para que siga el programa

                    if (response2['name'] and response3['name']):
                        #para la coleccion de archivo
                        try:
                            dataArchivo['file'] = files["File"].name
                            dataArchivo['sizeFile'] = files["File"].size
                            dataArchivo['format'] = files["File"].content_type
                            
                            response4 = AF.getDataBase().child("archivo").push(dataArchivo, idToken)
                            #para la coleccion de licencia
                            if (response3['name'] != True): #si es diferente a true significa que hay una cadena dando a entender que si se subio la licencia externa
                                dataLicencia['file'] = files["externalLicense"].name #entonces sabiendo esto, significa que existe algo en files["externalLicense"]
                                dataLicencia['sizeFile'] = files["externalLicense"].size
                                dataLicencia['format'] = files["externalLicense"].content_type

                                response5 = AF.getDataBase().child("licencia").push(dataLicencia, idToken)
                            else:
                                response5['name'] = True#Si no hay nada para externalLicense entonces le asignamos true para que siga el programa

                            if (response4['name'] and response5['name']):
                                try:
                                    data['Archivo'] = response4['name']

                                    if (response5['name'] != True):
                                        data['Licencia'] = response5['name']
                                    
                                    response6 = AF.getDataBase().child("proyecto").child(response['name']).update(data, idToken)
                                    if response6['title']:
                                        result['mensaje'] = 'Se creo el documento de forma exitosa!!'
                                        result['archivoAgregado'] = True
                                        result['error'] = False
                                        return result
                                    else:# si salio mal entonces eliminame los registros que se crearon
                                        AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                                        AF.getDataBase().child("archivo").child(response4['name']).remove(idToken)
                                        if (response5['name'] != True):#Si es diferente a true significa que si se creo el registro, por el cual debemos eliminarlo
                                            AF.getDataBase().child("licencia").child(response5['name']).remove(idToken)
                                            AF.getStorage().delete("pdf/" + response['name'] + "/" + files['externalLicense'].name, idToken)#tambien elimina los archivos del storage
                                        AF.getStorage().delete("pdf/" + response['name'] + "/" + files['File'].name, idToken)#tambien elimina los archivos del storage
                                        result['mensaje'] = 'No se actualizo el documento con los registros en las demas colecciones!!'
                                        result['archivoAgregado'] = False
                                        result['error'] = True
                                        return result
                                except Exception as e:# si salio mal entonces eliminame los registros que se crearon
                                    AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                                    AF.getDataBase().child("archivo").child(response4['name']).remove(idToken)
                                    if (response5['name'] != True):#Si es diferente a true significa que si se creo el registro, por el cual debemos eliminarlo
                                        AF.getDataBase().child("licencia").child(response5['name']).remove(idToken)
                                        AF.getStorage().delete("pdf/" + response['name'] + "/" + files['externalLicense'].name, idToken)#tambien elimina los archivos del storage
                                    AF.getStorage().delete("pdf/" + response['name'] + "/" + files['File'].name, idToken)#tambien elimina los archivos del storage
                                    result['mensaje'] = 'Ocurrio un error al intentar actualizar el documento con los registros en las demas colecciones!!'
                                    result['archivoAgregado'] = False
                                    result['error'] = True
                                    print(e)
                                    return result
                            else:# si salio algo mal entonces eliminame el primer registro que se creo
                                AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                                if (response3['name'] != True):#Si es diferente a true significa que si se creo el registro, por el cual debemos eliminarlo
                                    AF.getStorage().delete("pdf/" + response['name'] + "/" + files['externalLicense'].name, idToken)#tambien elimina los archivos del storage
                                AF.getStorage().delete("pdf/" + response['name'] + "/" + files['File'].name, idToken)#tambien elimina los archivos del storage
                                result['mensaje'] = 'No se creo la coleccion perteneciente al registro!!'
                                result['archivoAgregado'] = False
                                result['error'] = True
                                return result
                        except Exception as e:# si salio algo mal entonces eliminame el primer registro que se creo
                            AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                            if (response3['name'] != True):#Si es diferente a true significa que si se creo el registro, por el cual debemos eliminarlo
                                AF.getStorage().delete("pdf/" + response['name'] + "/" + files['externalLicense'].name, idToken)#tambien elimina los archivos del storage
                            AF.getStorage().delete("pdf/" + response['name'] + "/" + files['File'].name, idToken)#tambien elimina los archivos del storage
                            result['mensaje'] = 'Ocurrio un error al intentar crear la coleccion perteneciente al registro!!'
                            result['archivoAgregado'] = False
                            result['error'] = True
                            print(e)
                            return result
                    else:# si salio algo mal entonces eliminame el primer registro que se creo
                        AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                        if (response3['name'] != True):#Si es diferente a true significa que si se creo el registro, por el cual debemos eliminarlo
                            AF.getStorage().delete("pdf/" + response['name'] + "/" + files['externalLicense'].name, idToken)#tambien elimina los archivos del storage
                        AF.getStorage().delete("pdf/" + response['name'] + "/" + files['File'].name, idToken)#tambien elimina los archivos del storage
                        result['mensaje'] = 'No se subieron los archivos a la base de datos!!'
                        result['archivoAgregado'] = False
                        result['error'] = True
                        return result
                except Exception as e:
                    AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                    if (response3['name'] != True):#Si es diferente a true significa que si se creo el registro, por el cual debemos eliminarlo
                        AF.getStorage().delete("pdf/" + response['name'] + "/" + files['externalLicense'].name, idToken)#tambien elimina los archivos del storage
                    AF.getStorage().delete("pdf/" + response['name'] + "/" + files['File'].name, idToken)#tambien elimina los archivos del storage
                    result['mensaje'] = 'Ocurrio un error al intentar subir los archivos a la base de datos!!'
                    result['archivoAgregado'] = False
                    result['error'] = True
                    print(e)
                    return result
            else:
                result['mensaje'] = 'No se registro el documento!!'
                result['archivoAgregado'] = False
                result['error'] = True
                return result
        except Exception as e:
            result['mensaje'] = 'Ocurrio un error al registrar este documento!!'
            result['archivoAgregado'] = False
            result['error'] = True
            print(e)
            return result

    @staticmethod
    def contarDocumentos(nameFile):
        datosDeSesion = Documento.devolverTodosLosDatosSesion(nameFile)
        users = AF.getDataBase().child('proyecto').get(datosDeSesion['idToken']).val()
        cantidadDeUsuarios = len(users)
        return cantidadDeUsuarios

    @staticmethod
    def devolverTodosLosDatosSesion(nameFile):#aqui abrimos el json con los datos de session y 
        #lo retornamos para obtener los datos para otros metodos
        with open(nameFile + '.json') as file:
            data = json.load(file)
            return data
    
    @staticmethod
    def validarTipoProyecto(data, files):
        result = dict()
        if ('externalLicense' in files and data['typeProject'] == 'Proyecto externo'):
            result['error'] = False
            return result
        elif ('externalLicense' in files and data['typeProject'] == 'Proyecto interno'):
            result['error'] = True
            result['mensaje'] = 'No puede subir la licencia externa para un proyecto interno'
            #si el usuario trato de enviar un archivo de licencia cuando el proyecto es interno, entonces hay un error
            return result
        elif (not 'externalLicense' in files and data['typeProject'] == 'Proyecto interno'):# si de alguna forma no cumple con los dos anteriores y trata de hacer otra cosa, entonces hay un error
            result['error'] = False
            return result
        elif (not 'externalLicense' in files and data['typeProject'] == 'Proyecto externo'):# si de alguna forma no cumple con los dos anteriores y trata de hacer otra cosa, entonces hay un error
            result['error'] = True
            result['mensaje'] = 'No puede registrar un proyecto externo sin su licencia externa'
            return result
    
    @staticmethod
    def getDocumentos(idToken):
        result = dict()
        try:
            all_Documentos = AF.getDataBase().child('proyecto').get(idToken)
            listaDocumentos = list()
            data = dict()
            for qys in all_Documentos.each():
                data = qys.val()
                data['key'] = qys.key()
                listaDocumentos.append(data)
            result['listaDocumentos'] = listaDocumentos
            #print(listaQYS)
            result['error'] = False
            return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'No se obtuvieron los documentos en la base de datos!!'
            print(e)
            return result
