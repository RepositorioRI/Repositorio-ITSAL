
from datetime import datetime
import json
from repositorio.logic.atributosFirebase import AF
from django.core.files.uploadedfile import InMemoryUploadedFile


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
        if documentos == None:
            return 0
        else:
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
            if documentosQuimica == None:
                result['countQuimica'] = 0
            else:
                result['countQuimica'] = len(documentosQuimica)
            try:
                documentosElectronica = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IE).get().val()
                if documentosElectronica == None:
                    result['countElectronica'] = 0
                else:
                    result['countElectronica'] = len(documentosElectronica)
                try:
                    documentosMecanica = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IM).get().val()
                    if documentosMecanica == None:
                        result['countMecanica'] = 0
                    else:
                        result['countMecanica'] = len(documentosMecanica)
                    try:
                        documentosAcuicultura = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IA).get().val()
                        if documentosAcuicultura == None:
                            result['countAcuicultura'] = 0
                        else:
                            result['countAcuicultura'] = len(documentosAcuicultura)
                        try:
                            documentosIGE = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(IGE).get().val()
                            if documentosIGE == None:
                                result['countIGE'] = 0
                            else:
                                result['countIGE'] = len(documentosIGE)
                            try:
                                documentosTICS = AF.getDataBase().child("proyecto").order_by_child("career").equal_to(ITICS).get().val()
                                if documentosTICS == None:
                                    result['countTICS'] = 0
                                else:
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
    def validarTipoProyecto2(data, files, documento):
        result = dict()
        if (not 'File' in files and not 'externalLicense' in files and data['typeProject'] == 'Proyecto externo' and documento['typeProject'] == 'Proyecto externo'): #esta condicion es para editar un proyecto externo sin que este mande la licencia nuevamente
            result['error'] = False
            result['opcion'] = 1#editanto un proyecto externo sin subir licencia externa y sin suibr archivo (solo los campos)
            return result
        elif ('File' in files and not 'externalLicense' in files and data['typeProject'] == 'Proyecto externo' and documento['typeProject'] == 'Proyecto externo'):
            result['error'] = False
            result['opcion'] = 2#editanto un proyecto externo sin subir licencia externa, pero subiendo el archivo (cambiar los campos y el archivo)
            return result
        elif ('File' in files and 'externalLicense' in files and data['typeProject'] == 'Proyecto externo' and documento['typeProject'] == 'Proyecto externo'):
            result['error'] = False
            result['opcion'] = 3#editanto un proyecto externo, subiendo licencia externa y cambiando el archivo (cambiar todo)
            return result
        elif (not 'externalLicense' in files and data['typeProject'] == 'Proyecto externo' and documento['typeProject'] == 'Proyecto interno'): #en caso que el admin intente editar un proyecto interno a externo y que este no mande la licencia externa
            result['error'] = True
            result['mensaje'] = 'Esta cambiando un proyecto interno a uno externo, para ello debe subir la licencia'
            return result
        elif (not 'File' in files and 'externalLicense' in files and data['typeProject'] == 'Proyecto externo' and documento['typeProject'] == 'Proyecto interno'): #en este caso, esta intentando cambiar un proyecto interno a externo mandando la licencia externa
            result['error'] = False
            result['opcion'] = 4#editando un proyecto interno a un proyecto externo, subiendo la licencia, pero sin subir o cambiar el archivo
            return result
        elif ('File' in files and 'externalLicense' in files and data['typeProject'] == 'Proyecto externo' and documento['typeProject'] == 'Proyecto interno'):
            result['error'] = False
            result['opcion'] = 5#editando un proyecto interno a un proyecto externo, subiendo la licencia  y subiendo o cambiando el archivo
            return result
        elif (not 'File' in files and data['typeProject'] == 'Proyecto interno' and documento['typeProject'] == 'Proyecto externo'):
            result['error'] = False
            result['opcion'] = 6#editando un proyecto externo a un proyecto interno, sin subir el archivo, aqui se debe eliminar la licencia externa
            return result
        elif('File' in files and data['typeProject'] == 'Proyecto interno' and documento['typeProject'] == 'Proyecto externo'):
            result['error'] = False
            result['opcion'] = 7#editando un proyecto externo a un proyecto interno, pero subiendo o cambiando el archivo del proyecto, aqui se debe eliminar la licencia externa
            return result
        elif(not 'File' in files and not 'externalLicense' in files and data['typeProject'] == 'Proyecto interno' and documento['typeProject'] == 'Proyecto interno'):
            result['error'] = False
            result['opcion'] = 8#editando un proyecto interno sin subir o cambiar el archivo, obviamente sin subir licencia externa (solo cambiar campos)
            return result
        elif('externalLicense' in files and data['typeProject'] == 'Proyecto interno' and documento['typeProject'] == 'Proyecto interno'):
            result['error'] = True
            result['mensaje'] = 'Esta tratando de editar un proyecto interno, recuerde que los proyectos internos no llevan licencia externa'
            return result
        elif('File' in files and not 'externalLicense' in files and data['typeProject'] == 'Proyecto interno' and documento['typeProject'] == 'Proyecto interno'):
            result['error'] = False
            result['opcion'] = 9#editando un proyecto interno subiendo o cambiando de archivo, obviamente sin subir la licencia externa (campos mas archivo)
            return result
        else:
            result['error'] = True
            result['mensaje'] = 'Por favor verifique lo que esta haciendo, usted puede cambiar un proyecto interno a ser un proyecto externo y viceversa. Pero recuerde que para ello existen ciertas cuestiones...\n'+'1.- Los proyectos internos no tienen licencias externas \n2.- Los proyectos externos deben tener su licencia externa \n3.-Cualquier tipo de proyecto debe tener siempre su archivo'
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
    def editarDocumento(data, files, opcion, idToken, documento, key):
        if (opcion == 1):
            return Documento.opcion1Editar(data, files, idToken, documento, key)
        elif (opcion == 2):
            return Documento.opcion2Editar(data, files, idToken, documento, key)
        elif (opcion == 3):
            return Documento.opcion3Editar(data, files, idToken, documento, key)
        elif (opcion == 4):
            return Documento.opcion4Editar(data, files, idToken, documento, key)
        elif (opcion == 5):
            return Documento.opcion5Editar(data, files, idToken, documento, key)
        elif (opcion == 6):
            return Documento.opcion6Editar(data, files, idToken, documento, key)
        elif (opcion == 7):
            return Documento.opcion7Editar(data, files, idToken, documento, key)
        elif (opcion == 8):
            return Documento.opcion8Editar(data, files, idToken, documento, key)
        elif (opcion == 9):
            return Documento.opcion9Editar(data, files, idToken, documento, key)
        else:
            result = dict()
            result['error'] = True
            result['mensaje'] = 'Opcion desconocida!!'
            return result

    @staticmethod
    def opcion1Editar(data, files, idToken, documento, key):
        #editanto un proyecto externo sin subir licencia externa y sin suibr archivo (solo los campos)
        result = dict()
        try:
            response = AF.getDataBase().child("proyecto").child(key).update(data, idToken)
            result['error'] = False
            result['mensaje'] = 'Se editó con éxito el documento!!'
            return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se pudo editar el documento!!'
            return result
    
    @staticmethod
    def opcion2Editar(data, files, idToken, documento, key):
        #editanto un proyecto externo sin subir licencia externa, pero subiendo el archivo (cambiar los campos y el archivo)
        result = dict()
        try:
            #primero subimos el archivo nuevo para ello consultamos el archivo en la base de datos para traer el nombre del archivo
            archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
            try:
                #ahora eliminamos el archivo del storage
                AF.getStorage().delete("pdf/" + key + "/" + archivo['file'], idToken)
                try:
                    #ahora subimos el archivo nuevo
                    AF.getStorage().child("pdf/" + key + "/" + files['File'].name).put(files['File'], idToken)
                    try:
                        #ahora editamos el registro de la coleccion de archivo del database
                        dataArchivo = dict()
                        dataArchivo['file'] = files["File"].name
                        dataArchivo['sizeFile'] = files["File"].size
                        dataArchivo['format'] = files["File"].content_type
                        AF.getDataBase().child('archivo').child(documento['Archivo']).update(dataArchivo, idToken)
                        try:
                            #ahora editamos el proyecto
                            AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                            #si todo bien
                            result['error'] = False
                            result['mensaje'] = 'Se editó el documento con exitó!'
                            return result
                        except Exception as e:
                            print(e)
                            result['error'] = True
                            result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                            return result
                    except Exception as e:
                        print(e)
                        result['error'] = True
                        result['mensaje'] = 'No se pudo actualizar el registro de archivo de la base de datos!!'
                        return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se pudo subir el archivo nuevo asociado al proyecto en el almacenamiento'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo eliminar el archivo asociado al proyecto'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se encontro el archivo asociado al proyecto'
            return result

    @staticmethod
    def opcion3Editar(data, files, idToken, documento, key):
        #editanto un proyecto externo, subiendo licencia externa y cambiando el archivo (cambiar todo)
        result = dict()
        try:
            #consultamos el registro de licencia para obtener el nombre de la licencia
            licencia = AF.getDataBase().child('licencia').child(documento['Licencia']).get().val()
            try:
                #ahora eliminamos la licencia del storage
                AF.getStorage().delete("pdf/" + key + "/" + licencia['file'], idToken)
                try:
                    #ahora subimos la nueva licencia
                    AF.getStorage().child("pdf/" + key + "/" + files['externalLicense'].name).put(files['externalLicense'], idToken)
                    try:
                        #ahora editamos el registro de la coleccion de licencia del database
                        dataLicencia = dict()
                        dataLicencia['file'] = files["externalLicense"].name
                        dataLicencia['sizeFile'] = files["externalLicense"].size
                        dataLicencia['format'] = files["externalLicense"].content_type
                        AF.getDataBase().child('licencia').child(documento['Licencia']).update(dataLicencia, idToken)
                        try:
                            #ahora repetimos el mismo proceso ahora con archivo
                            archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
                            try:
                                #ahora eliminamos el archivo del storage
                                AF.getStorage().delete("pdf/" + key + "/" + archivo['file'], idToken)
                                try:
                                    #ahora subimos el archivo nuevo
                                    AF.getStorage().child("pdf/" + key + "/" + files['File'].name).put(files['File'], idToken)
                                    try:
                                        #ahora editamos el registro de la coleccion de archivo del database
                                        dataArchivo = dict()
                                        dataArchivo['file'] = files["File"].name
                                        dataArchivo['sizeFile'] = files["File"].size
                                        dataArchivo['format'] = files["File"].content_type
                                        AF.getDataBase().child('archivo').child(documento['Archivo']).update(dataArchivo, idToken)
                                        try:
                                            #ahora editamos el proyecto
                                            AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                                            #si todo bien
                                            result['error'] = False
                                            result['mensaje'] = 'Se editó el documento con exitó!'
                                            return result
                                        except Exception as e:
                                            print(e)
                                            result['error'] = True
                                            result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                                            return result
                                    except Exception as e:
                                        print(e)
                                        result['error'] = True
                                        result['mensaje'] = 'No se pudo actualizar el registro de archivo de la base de datos!!'
                                        return result
                                except Exception as e:
                                    print(e)
                                    result['error'] = True
                                    result['mensaje'] = 'No se pudo subir el archivo nuevo asociado al proyecto en el almacenamiento'
                                    return result
                            except Exception as e:
                                print(e)
                                result['error'] = True
                                result['mensaje'] = 'No se pudo eliminar el archivo asociado al proyecto'
                                return result
                        except Exception as e:
                            print(e)
                            result['error'] = True
                            result['mensaje'] = 'No se encontro el archivo asociado al proyecto'
                            return result
                    except Exception as e:
                        print(e)
                        result['error'] = True
                        result['mensaje'] = 'No se pudo actualizar el registro de licencia de la base de datos!!'
                        return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se pudo subir la nueva licencia asociado al proyecto en el almacenamiento'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo eliminar la licencia asociado al proyecto'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se encontro la licencia asociado al proyecto'
            return result

    @staticmethod
    def opcion4Editar(data, files, idToken, documento, key):
        #editando un proyecto interno a un proyecto externo, subiendo la licencia, pero sin subir o cambiar el archivo
        result = dict()
        try:
            #primero subimos la licencia al storage
            AF.getStorage().child("pdf/" + key + "/" + files['externalLicense'].name).put(files['externalLicense'], idToken)
            try:
                #ahora creamos el registro de la coleccion de licencia del database asociado a este proyecto
                dataLicencia = dict()
                dataLicencia['file'] = files["externalLicense"].name
                dataLicencia['sizeFile'] = files["externalLicense"].size
                dataLicencia['format'] = files["externalLicense"].content_type
                licencia = AF.getDataBase().child('licencia').push(dataLicencia, idToken)
                try:
                    #Ahora editamos el proyecto
                    data['Licencia'] = licencia['name']#le mandamos la key de la licencia que creamos para asociarlo al proyecto
                    AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                    #si todo bien
                    result['error'] = False
                    result['mensaje'] = 'Se editó el documento con exitó!'
                    return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo crear el registro de licencia de la base de datos!!'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se pudo subir la licencia asociado al proyecto'
            return result

    @staticmethod
    def opcion5Editar(data, files, idToken, documento, key):
        #editando un proyecto interno a un proyecto externo, subiendo la licencia  y subiendo o cambiando el archivo
        result = dict()
        try:
            #primero subimos la licencia al storage
            AF.getStorage().child("pdf/" + key + "/" + files['externalLicense'].name).put(files['externalLicense'], idToken)
            try:
                #ahora creamos el registro de la coleccion de licencia del database asociado a este proyecto
                dataLicencia = dict()
                dataLicencia['file'] = files["externalLicense"].name
                dataLicencia['sizeFile'] = files["externalLicense"].size
                dataLicencia['format'] = files["externalLicense"].content_type
                licencia = AF.getDataBase().child('licencia').push(dataLicencia, idToken)
                try:
                    #ahora consultamos el archivo del database para obtener el nombre
                    archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
                    try:
                        #ahora eliminamos el archivo del storage
                        AF.getStorage().delete("pdf/" + key + "/" + archivo['file'], idToken)
                        try:
                            #ahora subimos el archivo nuevo
                            AF.getStorage().child("pdf/" + key + "/" + files['File'].name).put(files['File'], idToken)
                            try:
                                #ahora editamos el registro de la coleccion de archivo del database
                                dataArchivo = dict()
                                dataArchivo['file'] = files["File"].name
                                dataArchivo['sizeFile'] = files["File"].size
                                dataArchivo['format'] = files["File"].content_type
                                AF.getDataBase().child('archivo').child(documento['Archivo']).update(dataArchivo, idToken)
                                try:
                                    #ahora editamos el proyecto
                                    data['Licencia'] = licencia['name']
                                    AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                                    #si todo bien
                                    result['error'] = False
                                    result['mensaje'] = 'Se editó el documento con exitó!'
                                    return result
                                except Exception as e:
                                    print(e)
                                    result['error'] = True
                                    result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                                    return result
                            except Exception as e:
                                print(e)
                                result['error'] = True
                                result['mensaje'] = 'No se pudo actualizar el registro de archivo de la base de datos!!'
                                return result
                        except Exception as e:
                            print(e)
                            result['error'] = True
                            result['mensaje'] = 'No se pudo subir el archivo nuevo asociado al proyecto en el almacenamiento'
                            return result
                    except Exception as e:
                        print(e)
                        result['error'] = True
                        result['mensaje'] = 'No se pudo eliminar el archivo asociado al proyecto'
                        return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se encontro el archivo asociado al proyecto'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo crear el registro de licencia de la base de datos!!'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se pudo subir la licencia asociado al proyecto'
            return result

    @staticmethod
    def opcion6Editar(data, files, idToken, documento, key):
        #editando un proyecto externo a un proyecto interno, sin subir el archivo, aqui se debe eliminar la licencia externa
        result = dict()
        try:
            #primero consultamos la licencia del database para obtener el nombre
            licencia = AF.getDataBase().child('licencia').child(documento['Licencia']).get().val()
            try:
                #ahora eliminamos la licencia del storage
                AF.getStorage().delete("pdf/" + key + "/" + licencia['file'], idToken)
                try:
                    #ahora eliminamos el registro de licencia de la base de datos
                    AF.getDataBase().child('licencia').child(documento['Licencia']).remove(idToken)
                    try:
                        #ahora editamos el proyecto
                        data['Licencia'] = None #para que elimine el campo Licencia
                        AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                        #si todo bien
                        result['error'] = False
                        result['mensaje'] = 'Se editó el documento con exitó!'
                        return result
                    except Exception as e:
                        print(e)
                        result['error'] = True
                        result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                        return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se pudo eliminar el registro de licencia de la base de datos!!'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo eliminar la licencia asociado al proyecto'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se encontro la licencia asociado al proyecto'
            return result
            

    @staticmethod
    def opcion7Editar(data, files, idToken, documento, key):
        #editando un proyecto externo a un proyecto interno, pero subiendo o cambiando el archivo del proyecto, aqui se debe eliminar la licencia externa
        result = dict()
        try:
            #primero consultamos la licencia del database para obtener el nombre
            licencia = AF.getDataBase().child('licencia').child(documento['Licencia']).get().val()
            try:
                #ahora eliminamos la licencia del storage
                AF.getStorage().delete("pdf/" + key + "/" + licencia['file'], idToken)
                try:
                    #ahora eliminamos el registro de licencia de la base de datos
                    AF.getDataBase().child('licencia').child(documento['Licencia']).remove(idToken)
                    try:
                        #ahora queda cambiar el archivo para ello primero consultamos el archivo que tenemos para eliminarlo
                        archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
                        try:
                            #ahora eliminamos el archivo del storage
                            AF.getStorage().delete("pdf/" + key + "/" + archivo['file'], idToken)
                            try:
                                #ahora subimos el archivo nuevo
                                AF.getStorage().child("pdf/" + key + "/" + files['File'].name).put(files['File'], idToken)
                                try:
                                    #ahora editamos el registro de la coleccion de archivo del database
                                    dataArchivo = dict()
                                    dataArchivo['file'] = files["File"].name
                                    dataArchivo['sizeFile'] = files["File"].size
                                    dataArchivo['format'] = files["File"].content_type
                                    AF.getDataBase().child('archivo').child(documento['Archivo']).update(dataArchivo, idToken)
                                    try:
                                        #ahora editamos el proyecto
                                        data['Licencia'] = None
                                        AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                                        #si todo bien
                                        result['error'] = False
                                        result['mensaje'] = 'Se editó el documento con exitó!'
                                        return result
                                    except Exception as e:
                                        print(e)
                                        result['error'] = True
                                        result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                                        return result
                                except Exception as e:
                                    print(e)
                                    result['error'] = True
                                    result['mensaje'] = 'No se pudo actualizar el registro de archivo de la base de datos!!'
                                    return result
                            except Exception as e:
                                print(e)
                                result['error'] = True
                                result['mensaje'] = 'No se pudo subir el archivo nuevo asociado al proyecto en el almacenamiento'
                                return result
                        except Exception as e:
                            print(e)
                            result['error'] = True
                            result['mensaje'] = 'No se pudo eliminar el archivo asociado al proyecto'
                            return result
                    except Exception as e:
                        print(e)
                        result['error'] = True
                        result['mensaje'] = 'No se encontro el archivo asociado al proyecto'
                        return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se pudo eliminar el registro de licencia de la base de datos!!'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo eliminar la licencia asociado al proyecto'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se encontro la licencia asociado al proyecto'
            return result

    @staticmethod
    def opcion8Editar(data, files, idToken, documento, key):
        #editando un proyecto interno sin subir o cambiar el archivo, obviamente sin subir licencia externa (solo cambiar campos)
        result = dict()
        try:
            #solamente editamos el proyecto
            AF.getDataBase().child('proyecto').child(key).update(data, idToken)
            #si todo bien
            result['error'] = False
            result['mensaje'] = 'Se editó el documento con exitó!'
            return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
            return result

    @staticmethod
    def opcion9Editar(data, files, idToken, documento, key):
        #editando un proyecto interno subiendo o cambiando de archivo, obviamente sin subir la licencia externa (campos mas archivo)
        result = dict()
        try:
            #consultamos el archivo de la base de datos para conseguir el nombre y asi eliminarlo de storage
            archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
            try:
                #ahora eliminamos el archivo del storage
                AF.getStorage().delete("pdf/" + key + "/" + archivo['file'], idToken)
                try:
                    #ahora subimos el archivo nuevo
                    AF.getStorage().child("pdf/" + key + "/" + files['File'].name).put(files['File'], idToken)
                    try:
                        #ahora editamos el registro de la coleccion de archivo del database
                        dataArchivo = dict()
                        dataArchivo['file'] = files["File"].name
                        dataArchivo['sizeFile'] = files["File"].size
                        dataArchivo['format'] = files["File"].content_type
                        AF.getDataBase().child('archivo').child(documento['Archivo']).update(dataArchivo, idToken)
                        try:
                            #ahora editamos el proyecto
                            AF.getDataBase().child('proyecto').child(key).update(data, idToken)
                            #si todo bien
                            result['error'] = False
                            result['mensaje'] = 'Se editó el documento con exitó!'
                            return result
                        except Exception as e:
                            print(e)
                            result['error'] = True
                            result['mensaje'] = 'No se pudo actualizar el registro de proyecto de la base de datos!!'
                            return result
                    except Exception as e:
                        print(e)
                        result['error'] = True
                        result['mensaje'] = 'No se pudo actualizar el registro de archivo de la base de datos!!'
                        return result
                except Exception as e:
                    print(e)
                    result['error'] = True
                    result['mensaje'] = 'No se pudo subir el archivo nuevo asociado al proyecto en el almacenamiento'
                    return result
            except Exception as e:
                print(e)
                result['error'] = True
                result['mensaje'] = 'No se pudo eliminar el archivo asociado al proyecto'
                return result
        except Exception as e:
            print(e)
            result['error'] = True
            result['mensaje'] = 'No se encontro el archivo asociado al proyecto'
            return result
    
    @staticmethod
    def sonIguales(files):
        if ('File' in files and 'externalLicense' in files):
            if isinstance(files['File'], InMemoryUploadedFile) and isinstance(files['externalLicense'], InMemoryUploadedFile):
                if files['File'].size != files['externalLicense'].size:
                    return False

                file1_content = files['File'].read()
                file2_content = files['externalLicense'].read()

                return file1_content == file2_content
            return False
        return False

    @staticmethod
    def sonIguales2(files, documento):
        if ('File' in files and 'externalLicense' in files):#aqui entra si trato de editar dos archivos por ende esos los recibimos en el request
            if isinstance(files['File'], InMemoryUploadedFile) and isinstance(files['externalLicense'], InMemoryUploadedFile):
                if files['File'].size != files['externalLicense'].size:
                    return False

                file1_content = files['File'].read()
                file2_content = files['externalLicense'].read()

                return file1_content == file2_content
            return False
        elif ('externalLicense' in files):
            #consultamos los datos del archivo para comparar con el que estamos recibiendo en licencia externa
            try:
                archivo = AF.getDataBase().child('archivo').child(documento['Archivo']).get().val()
                if (archivo['file'] == files["externalLicense"].name and archivo['sizeFile'] == files["externalLicense"].size):
                    return True
                else:
                    return False
            except Exception as e:
                print(e)
        elif ('File' in files):
            #en caso que el usuario este editando un proyecto externo, primero debemos asegurarnos que este proyecto si es externo para ello validamos que si el documento tiene licencia
            if ('Licencia' in documento):
                try:
                    licencia = AF.getDataBase().child('licencia').child(documento['Licencia']).get().val()
                    if (licencia['file'] == files["File"].name and licencia['sizeFile'] == files["File"].size):
                        return True
                    else:
                        return False
                except Exception as e:
                    print(e)
        else:
            #si llega hasta aqui significa que no quiere editar los archivos, solo los campos, por ello retornamos un false
            return False
