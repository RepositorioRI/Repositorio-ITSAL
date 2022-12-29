from django.urls import path
from .  import views

urlpatterns = [
       path('', views.index),
       path('login/', views.login),
       path('logout/', views.logout),
       path('inicioAdminSubadmin/', views.inicioAdminSubadmin),
       path('contacto/', views.contacto),
       path('registroSub/', views.registroSub),
       path('agregarDocumentos/', views.agregarDocumentos),
]