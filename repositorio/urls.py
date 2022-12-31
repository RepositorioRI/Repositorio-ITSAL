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
       path('vistaDocumento/', views.vistaDocumento, name="vistaDocumento"),
        path('vistaMetadatos/', views.vistaMetadatos, name="vistaMetadatos"),
]