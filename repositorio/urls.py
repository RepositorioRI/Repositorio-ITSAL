from django.urls import path
from .  import views

urlpatterns = [
       path('', views.inicio, name="inicio"),
       path('login/', views.login, name="login"),
       path('logout/', views.logout, name="logout"),
       path('inicioAdminSubadmin/', views.inicioAdminSubadmin, name="inicioAdminSubadmin"),
       path('contacto/', views.contacto, name="contacto"),
       path('registroSub/', views.registroSub, name="registroSub"),
       path('agregarDocumentos/', views.agregarDocumentos, name="agregarDocumentos"),
       path('vistaDocumento/<str:key>', views.vistaDocumento, name="vistaDocumento"),
       path('vistaMetadatos/<str:key>', views.vistaMetadatos, name="vistaMetadatos"),
       path('vistaSubadministradores/', views.vistaSubadministradores, name="vistaSubadministradores"),
       path('vistaQuejasSugerencias/', views.vistaQuejasSugerencias, name="vistaQuejasSugerencias"),
       path('vistaDocumentos/', views.vistaDocumentosTodos, name="vistaDocumentos"),
       path('eliminarQYS/<str:key>', views.eliminarQYS, name="eliminarQYS"),
       path('eliminarUsuario/<str:key>', views.eliminarUsuario, name="eliminarUsuario"),
       path('cuentaInhabilitada/', views.cuentaInhabilitada, name="cuentaInhabilitada"),
       path('vistaDocumentoCarrera/<str:career>', views.vistaDocumentosCarrera, name="vistaDocumentoCarrera"),
       
]

