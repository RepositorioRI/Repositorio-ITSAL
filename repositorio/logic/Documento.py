
import json
from repositorio.logic.atributosFirebase import AF


class Documento:

    @staticmethod
    def agregarDocumento(data, files, idToken):
        result = dict()
        try:
            response = AF.getDataBase().child("proyecto").push(data, idToken)
            if response['name']:
                try:
                    dataArchivo = dict()
                    dataLicencia = dict()
                    response2 = AF.getStorage().child("pdf/" + response['name'] + "/" + files['File'].name).put(files['File'], idToken)
                    response3 = AF.getStorage().child("pdf/" + response['name'] + "/" + files['externalLicense'].name).put(files['externalLicense'], idToken)

                    if (response2['name'] and response3['name']):
                        #para la coleccion de archivo
                        try:
                            dataArchivo['file'] = files["File"].name
                            dataArchivo['sizeFile'] = files["File"].size
                            dataArchivo['format'] = files["File"].content_type
                            #para la coleccion de licencia
                            dataLicencia['file'] = files["externalLicense"].name
                            dataLicencia['sizeFile'] = files["externalLicense"].size
                            dataLicencia['format'] = files["externalLicense"].content_type

                            response4 = AF.getDataBase().child("archivo").push(dataArchivo, idToken)
                            response5 = AF.getDataBase().child("licencia").push(dataLicencia, idToken)

                            if (response4['name'] and response5['name']):
                                try:
                                    data['Archivo'] = response4['name']
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
                                        AF.getDataBase().child("licencia").child(response5['name']).remove(idToken)
                                        result['mensaje'] = 'No se actualizo el documento con los registros en las demas colecciones!!'
                                        result['archivoAgregado'] = False
                                        result['error'] = True
                                        return result
                                except Exception as e:# si salio mal entonces eliminame los registros que se crearon
                                    AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                                    AF.getDataBase().child("archivo").child(response4['name']).remove(idToken)
                                    AF.getDataBase().child("licencia").child(response5['name']).remove(idToken)
                                    result['mensaje'] = 'Ocurrio un error al intentar actualizar el documento con los registros en las demas colecciones!!'
                                    result['archivoAgregado'] = False
                                    result['error'] = True
                                    print(e)
                                    return result
                            else:# si salio algo mal entonces eliminame el primer registro que se creo
                                AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                                result['mensaje'] = 'No se creo la coleccion perteneciente al registro!!'
                                result['archivoAgregado'] = False
                                result['error'] = True
                                return result
                        except Exception as e:# si salio algo mal entonces eliminame el primer registro que se creo
                            AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                            result['mensaje'] = 'Ocurrio un error al intentar crear la coleccion perteneciente al registro!!'
                            result['archivoAgregado'] = False
                            result['error'] = True
                            print(e)
                            return result
                    else:# si salio algo mal entonces eliminame el primer registro que se creo
                        AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
                        result['mensaje'] = 'No se subieron los archivos a la base de datos!!'
                        result['archivoAgregado'] = False
                        result['error'] = True
                        return result
                except Exception as e:
                    AF.getDataBase().child("proyecto").child(response['name']).remove(idToken)
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