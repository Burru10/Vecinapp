from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return render(request, "Vecinapp/index.html")

def servicios(request):
    return render(request, "Vecinapp/servicios.html")

def comunidad(request):
    return render(request, "Vecinapp/comunidad.html")

def sobre_nosotros(request):
    return render(request, "Vecinapp/sobre-nosotros.html")