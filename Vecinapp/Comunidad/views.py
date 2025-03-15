from django.shortcuts import render

# Create your views here.
def comunidad(request):
     return render(request, "Comunidad/comunidad.html")