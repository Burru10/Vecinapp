from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComunidadForm, PublicacionForm
from .models import Administrador, Comunidad, Publicacion, CategoriaTarea
from django.views.decorators.http import require_POST


def crear_comunidad(request):
    if request.method == "POST":
        form = ComunidadForm(request.POST)
        if form.is_valid(): 
            comunidad = form.save(commit=False)
            
            comunidad.administrador, _ = Administrador.objects.get_or_create(user=request.user)

            comunidad.save()
            comunidad.usuarios.add(request.user)
            return redirect("comunidad")
    
    return render(request, "comunidad/crear_comunidad.html", {"form": ComunidadForm()})


# Vista de la página principal de comunidad
def comunidad(request):
    comunidades_usuario = request.user.comunidades.all()

    # Se controla el caso en el que el usuario solo pertenezca a una comunidad, para enviarle directamente a la página de su comunidad
    if comunidades_usuario.count() == 1:
        return redirect("mi_comunidad", comunidad_id=comunidades_usuario.first().id)
    
    # Se controla el caso en el que el usuario no pertenezca a ninguna comunidad, para enviarle a la página de creación de comunidad
    if comunidades_usuario.count() == 0:
        return render(request, "comunidad/comunidad.html")

    # Se controla el caso en el que el usuario pertenezca a más de una comunidad, para enviarle a la página de selección de comunidad
    return render(request, "comunidad/mis_comunidades.html", {"comunidades": comunidades_usuario})


# Vista de la página de la comunidad
def mi_comunidad(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    publicaciones = Publicacion.objects.filter(comunidad=comunidad)

    #Oculta las tareas propias del usuario
    publicaciones = publicaciones.exclude(usuario=request.user)

    publicaciones = publicaciones.exclude(estado="completada")

    categoria_id = request.GET.get("categoria")
    if categoria_id:
        publicaciones = publicaciones.filter(categoria_id=categoria_id)

    if request.method == "POST":
        form = PublicacionForm(request.POST)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.comunidad = comunidad
            publicacion.save()
            return redirect('mi_comunidad', comunidad_id=comunidad.id)
    else:
        form = PublicacionForm()

    categorias = CategoriaTarea.objects.all()

    return render(
        request, 
        "comunidad/mi_comunidad.html", 
        {
            "comunidad": comunidad,
            "publicaciones": publicaciones,
            "form": form,
            "categorias": categorias,
        }
    )


#Vista para realizar tareas
@require_POST
def realizar_tarea(request, tarea_id):
    tarea = get_object_or_404(Publicacion, id=tarea_id, estado="abierta")

    if tarea.usuario!= request.user:
        tarea.estado = "en progreso"
        tarea.realizada_por = request.user
        tarea.save()

    return redirect("mi_comunidad", comunidad_id=tarea.comunidad.id)
    