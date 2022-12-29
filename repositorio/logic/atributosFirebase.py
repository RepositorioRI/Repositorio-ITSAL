import pyrebase;

class AF: # esta es la clase que contiene la conexion con el firebase

    __config = {#en esta variable tenemos todo acerca del proyecto en firebase para su conexion
        "apiKey": "AIzaSyA3OGyVvih90GDptfLTidJYI6J3UewAJjU",
        "authDomain": "repositorioitsal.firebaseapp.com",
        "databaseURL": "https://repositorioitsal-default-rtdb.firebaseio.com",
        "projectId": "repositorioitsal",
        "storageBucket": "repositorioitsal.appspot.com",
        "messagingSenderId": "886860742942",
        "appId": "1:886860742942:web:b6c6ae77d9c281a0ad090f"
    }
    #inicializamos la aplicacion de firebase en nuestro programa y lo guardamos en la variable __firebase
    __firebase = pyrebase.initialize_app(__config)
    #inicializamos la autenticacion del firebase y la guardamos en la variable __auth
    __auth = __firebase.auth()
    #inicializamos la base de datos del firebase y la guardamos en la variable __database
    __database = __firebase.database()
    #inicializamos el almacenamiento del firebase y la guardamos en la variable __storage
    __storage = __firebase.storage()

    #usamos el encapsulamiento para mejor practica
    @staticmethod
    def getFirebase():
        return AF.__firebase

    @staticmethod
    def getAuth(): 
        return AF.__auth

    @staticmethod
    def getDataBase():
        return AF.__database

    @staticmethod
    def getStorage():
        return AF.__storage
