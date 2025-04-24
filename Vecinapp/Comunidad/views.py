from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComunidadForm, PublicacionForm
from .models import Administrador, Comunidad, Publicacion, CategoriaTarea, SolicitudUnion
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
    

def salir_comunidad(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    comunidad.usuarios.remove(request.user)
    messages.success(request, "Has salido de la comunidad.")
    return redirect('comunidad')


def buscar_comunidades(request):
    query = request.GET.get("localidad", "")
    comunidades = Comunidad.objects.filter(localidad__icontains=query).exclude(usuarios=request.user) if query else []

    # Todas las solicitudes del usuario
    solicitudes = SolicitudUnion.objects.filter(usuario=request.user).order_by('-fecha')

    solicitud_map = {}

    for s in solicitudes:
        if s.comunidad_id not in solicitud_map:
            pertenece = s.comunidad.usuarios.filter(id=request.user.id).exists()
            if s.aceptada is True and not pertenece:
                continue  # ignoramos esta solicitud aceptada
            solicitud_map[s.comunidad_id] = s.aceptada

    # Añadir estado a cada comunidad listada
    for c in comunidades:
        c.estado_solicitud = solicitud_map.get(c.id, "no_solicitud")

    return render(request, "comunidad/buscar.html", {
        "query": query,
        "resultados": comunidades
    })


def solicitar_union_ajax(request, comunidad_id):
    if request.method == "POST":
        comunidad = get_object_or_404(Comunidad, id=comunidad_id)

        if comunidad.usuarios.filter(id=request.user.id).exists():
            return JsonResponse({"status": "ya_miembro"})

        ultima = SolicitudUnion.objects.filter(usuario=request.user, comunidad=comunidad).order_by('-fecha').first()

        if ultima:
            if ultima.aceptada is None:
                return JsonResponse({"status": "pendiente"})
            elif ultima.aceptada is False:
                # ❗️ Crear una nueva solicitud permitida tras rechazo
                SolicitudUnion.objects.create(usuario=request.user, comunidad=comunidad, aceptada=None)
                return JsonResponse({"status": "pendiente"})
            elif ultima.aceptada is True and not comunidad.usuarios.filter(id=request.user.id).exists():
                SolicitudUnion.objects.create(usuario=request.user, comunidad=comunidad, aceptada=None)
                return JsonResponse({"status": "pendiente"})

        # Crear nueva solicitud por defecto
        SolicitudUnion.objects.create(usuario=request.user, comunidad=comunidad, aceptada=None)
        return JsonResponse({"status": "pendiente"})

    return JsonResponse({"status": "error"})