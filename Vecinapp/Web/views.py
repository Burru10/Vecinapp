from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return render(request, "Vecinapp/index.html")

def contacto(request):
    return render(request, "Vecinapp/contacto.html")

def servicios(request):
    return render(request, "Vecinapp/servicios.html")

def solicitudes(request):
    return render(request, "Vecinapp/solicitudes.html")

def sobre_nosotros(request):
    return render(request, "Vecinapp/sobre-nosotros.html")