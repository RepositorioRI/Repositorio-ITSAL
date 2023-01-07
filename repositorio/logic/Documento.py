
from datetime import datetime
import json
from repositorio.logic.atributosFirebase import AF
import asyncio


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
    def contarDocumentos():
        documentos = AF.getDataBase().child('proyecto').get().val()
        cantidadDeDocumentos = len(documentos)
        return cantidadDeDocumentos

    @staticmethod
    def contarPorCarrera():
        result = dict()
        IQ = "Ing. Química"
        IE = "Ing. Electrónica"
        IM = "Ing. Mecánica"
        IA = "Ing. Acuicultura"
        IGE = "Ing. Gestión Empresarial"
        ITICS = "Ing. TIC'S"
        try:
            documentosQuimica = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IQ).get().val()
            result['countQuimica'] = len(documentosQuimica)
            try:
                documentosElectronica = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IE).get().val()
                result['countElectronica'] = len(documentosElectronica)
                try:
                    documentosMecanica = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IM).get().val()
                    result['countMecanica'] = len(documentosMecanica)
                    try:
                        documentosAcuicultura = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IA).get().val()
                        result['countAcuicultura'] = len(documentosAcuicultura)
                        try:
                            documentosIGE = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IGE).get().val()
                            result['countIGE'] = len(documentosIGE)
                            try:
                                documentosTICS = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(ITICS).get().val()
                                result['countTICS'] = len(documentosTICS)
                                result['error'] = False
                                return result
                            except Exception as e:
                                result['error'] = True
                                result['mensaje'] = 'No se obtuvieron la cantidad de documentos para la carrera de TICS'
                                print(e)
                                return result
                        except Exception as e:
                            result['error'] = True
                            result['mensaje'] = 'No se obtuvieron la cantidad de documentos para la carrera de IGE'
                            print(e)
                            return result
                    except Exception as e:
                        result['error'] = True
                        result['mensaje'] = 'No se obtuvieron la cantidad de documentos para la carrera de Acuicultura'
                        print(e)
                        return result
                except Exception as e:
                    result['error'] = True
                    result['mensaje'] = 'No se obtuvieron la cantidad de documentos para la carrera de Mecanica'
                    print(e)
                    return result
            except Exception as e:
                result['error'] = True
                result['mensaje'] = 'No se obtuvieron la cantidad de documentos para la carrera de Electronica'
                print(e)
                return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'No se obtuvieron la cantidad de documentos para la carrera de Quimica'
            print(e)
            return result
    
    @staticmethod
    def getPorCarrera(career):
        result = dict()
        try:
            tblCarrera = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(career).get()
            listaDocumentos = list()
            data = dict()
            for documento in tblCarrera.each():
                data = documento.val()
                data['key'] = documento.key()
                listaDocumentos.append(data)
            result['tblCarrera'] = listaDocumentos
            result['error'] = False
            return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'Error al obtener los proyectos de esa carrera!!'
            print(e)
            return result

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
    
    @staticmethod
    def getPorCategoria(type):
        result = dict()
        try:
            tblCategoria = AF.getDataBase().child("proyecto").order_by_child("type").equal_to(type).get()
            listaCategorias = list()
            data = dict()
            for documento in tblCategoria.each():
                data = documento.val()
                data['key'] = documento.key()
                listaCategorias.append(data)
            result['tblCategoria'] = listaCategorias
            result['error'] = False
            return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'Error al obtener los proyectos de esa categoría!!'
            print(e)
            return result

    @staticmethod
    def getDocumento(key):
        result = dict()
        try:
            documento = AF.getDataBase().child('proyecto').child(key).get().val()
            #print(documento)
            try:
                archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
                #print('encontro el archivo')
                megabits = archivo['sizeFile'] / 1048576
                megabits_redondeados = round(megabits, 2)
                try:
                    linkArchivo = AF.getStorage().child("pdf/" + key + "/" + archivo['file']).get_url('')
                    #print(linkArchivo)
                    if ('Licencia' in documento):
                        try:
                            #print('existe licencia')
                            licencia = AF.getDataBase().child('licencia').child(documento['Licencia']).get().val()
                            if (licencia['file']):
                                try:
                                    linkLicencia = AF.getStorage().child("pdf/" + key + "/" + licencia['file']).get_url('')
                                    result['error'] = False
                                    result['licencia'] = licencia
                                    result['documento'] = documento
                                    result['archivo'] = archivo
                                    result['linkArchivo'] = linkArchivo
                                    result['linkLicencia'] = linkLicencia
                                    result['keyDocumento'] = key
                                    result['megabits_redondeados'] = megabits_redondeados
                                    return result
                                except Exception as e:
                                    result['error'] = True
                                    result['mensaje'] = 'No se pudo obtener la licencia del storage!!'
                                    print(e)
                                    return result
                        except Exception as e:
                            #print('entro aqui')
                            result['error'] = True
                            result['mensaje'] = 'No se encontro la licencia externa asociado al proyecto!!'
                            print(e)
                            return result
                    else:
                        #print('Sin licencia externa')
                        result['error'] = False
                        result['documento'] = documento
                        result['archivo'] = archivo
                        result['linkArchivo'] = linkArchivo
                        result['keyDocumento'] = key
                        result['megabits_redondeados'] = megabits_redondeados
                        return result
                except Exception as e:
                    result['error'] = True
                    result['mensaje'] = 'No se obtuvo el link del archivo!!'
                    print(e)
                    return result
            except Exception as e:
                result['error'] = True
                result['mensaje'] = 'No hay archivo para este proyecto!!'
                print(e)
                return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'Ocurrio un error al obtener el proyecto!!'
            print(e)
            #print('entro en la excepcion')
            return result
    
    @staticmethod
    def esKeyValida(key):
        try:
            keys = AF.getDataBase().child('proyecto').get()
            #print(keys)
            for documento in keys.each():
                cadaKey = documento.key()
                if (cadaKey == key):
                    return True
            return False
        except:
            print('No se obtuvieron las keys')

    @staticmethod
    def esCarreraValida(career):
        carreras = dict()
        carreras['IQ'] = "Ing. Química"
        carreras['IE'] = "Ing. Electrónica"
        carreras['IM'] = "Ing. Mecánica"
        carreras['IA'] = "Ing. Acuicultura"
        carreras['IGE'] = "Ing. Gestión Empresarial"
        carreras['ITICS'] = "Ing. TIC'S"

        for clave in carreras:
            if(carreras[clave] == career):
                return True
            #print(carreras[clave])
        return False

    @staticmethod
    def esCategoriaValida(type):
        categorias = dict()
        categorias['RR'] = 'Reportes de residencia'
        categorias['T'] = 'Tesis'
        categorias['PRI'] = 'Proyectos integrales'

        for clave in categorias:
            if(categorias[clave] == type):
                return True
            #print(carreras[clave])
        return False
    
    @staticmethod
    def eliminarDocumento(idToken, key):
        result = dict()
        try:
            documento = AF.getDataBase().child('proyecto').child(key).get().val()
            if 'Licencia' in documento:
                try:
                    licencia = AF.getDataBase().child('licencia').child(documento['Licencia']).get().val()
                    try:
                        AF.getStorage().delete("pdf/" + key + "/" + licencia['file'], idToken)
                    except Exception as e:
                        result['error'] = True
                        result['mensaje'] = 'No se pudo eliminar la licencia del almacenamiento!!'
                        print(e)
                        return result
                    try:
                        AF.getDataBase().child("licencia").child(documento['Licencia']).remove(idToken)#estamos eliminando por eso mandamos el token
                    except Exception as e:
                        result['error'] = True
                        result['mensaje'] = 'No se elimino el registro de licencia en la base de datos!!'
                        print(e)
                        return result
                except Exception as e:
                    result['error'] = True
                    result['mensaje'] = 'No se encontro la licencia asociada al proyecto!!'
                    print(e)
                    return result
            try:
                archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
                try:
                    AF.getStorage().delete("pdf/" + key + "/" + archivo['file'], idToken)
                except Exception as e:
                    result['error'] = True
                    result['mensaje'] = 'No se pudo eliminar el archivo del almacenamiento!!'
                    print(e)
                    return result
                try:
                    AF.getDataBase().child("archivo").child(documento['Archivo']).remove(idToken)#estamos eliminando por eso mandamos el token
                except Exception as e:
                    result['error'] = True
                    result['mensaje'] = 'No se elimino el registro de archivo en la base de datos!!'
                    print(e)
                    return result
            except Exception as e:
                result['error'] = True
                result['mensaje'] = 'No se encontro el archivo asociado al proyecto!!'
                print(e)
                return result
            #si todo fue bien, entonces seguimos desde aqui
            try:
                AF.getDataBase().child("proyecto").child(key).remove(idToken)#estamos eliminando por eso mandamos el token
                result['error'] = False
                result['mensaje'] = 'Se elimino el documento de forma exitosa!!'
                return result
            except Exception as e:
                result['error'] = True
                result['mensaje'] = 'No se elimino el proyecto!!'
                print(e)
                return result
        except Exception as e:
            result['error'] = True
            result['mensaje'] = 'No se encontro el proyecto asociado!!'
            print(e)
            return result

    @staticmethod
    def editarDocumento(data, files, idToken):
        pass
