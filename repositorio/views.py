
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def inicioAdminSubadmin(request):
    return render(request,'inicioAdminSubadmin.html')

def contacto(request):
    return render(request,'contacto.html')

def registroSub(request):
    return render(request,'registroSub.html')

def agregarDocumentos(request):
    return render(request,'agregarDocumentos.html')