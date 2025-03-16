from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ComunidadForm
from .models import Administrador

def crear_comunidad(request):
    if request.method == "POST":
        form = ComunidadForm(request.POST)
        if form.is_valid():
            comunidad = form.save(commit=False)
            
            comunidad.administrador, _ = Administrador.objects.get_or_create(user=request.user)

            comunidad.save()
            comunidad.usuarios.add(request.user)
            messages.success(request, "Comunidad creada exitosamente.")
            return redirect("comunidad")
    
    return render(request, "comunidad/crear_comunidad.html", {"form": ComunidadForm()})

# Vista de la página principal de comunidad
def comunidad(request):
    return render(request, "comunidad/comunidad.html")
