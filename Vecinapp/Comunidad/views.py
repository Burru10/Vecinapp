from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComunidadForm, PublicacionForm
from .models import Administrador, Comunidad, Publicacion, CategoriaTarea, SolicitudUnion, SalidaUnion, AdminCambio, NotificacionSalida, Expulsion
from django.contrib.auth.models import User
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

    # NOTIFICACIONES
    user_notif_count = SolicitudUnion.objects.filter(
        comunidad=comunidad,
        usuario=request.user,
        aceptada__isnull=False,
        visto_usuario=False
    ).count()
    admin_notif_count = 0
    if comunidad.administrador.user == request.user:
        admin_notif_count = SolicitudUnion.objects.filter(
            comunidad=comunidad,
            aceptada__isnull=True
        ).count()

    return render(
        request, 
        "comunidad/mi_comunidad.html", 
        {
            "comunidad": comunidad,
            "publicaciones": publicaciones,
            "form": form,
            "categorias": categorias,
            "user_notif_count": user_notif_count,
            "admin_notif_count": admin_notif_count,
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
                # Crear una nueva solicitud permitida tras rechazo
                SolicitudUnion.objects.create(usuario=request.user, comunidad=comunidad, aceptada=None)
                return JsonResponse({"status": "pendiente"})
            elif ultima.aceptada is True and not comunidad.usuarios.filter(id=request.user.id).exists():
                SolicitudUnion.objects.create(usuario=request.user, comunidad=comunidad, aceptada=None)
                return JsonResponse({"status": "pendiente"})

        # Crear nueva solicitud por defecto
        SolicitudUnion.objects.create(usuario=request.user, comunidad=comunidad, aceptada=None)
        return JsonResponse({"status": "pendiente"})

    return JsonResponse({"status": "error"})


def mis_tareas(request):
    # Tareas que yo he publicado
    published = Publicacion.objects.filter(usuario=request.user)
    # Tareas que yo estoy realizando o he completado
    in_progress = Publicacion.objects.filter(realizada_por=request.user)
    return render(request, 'comunidad/mis_tareas.html', {
        'published': published,
        'in_progress': in_progress
    })


def ver_tarea(request, tarea_id):
    tarea = get_object_or_404(Publicacion, id=tarea_id)
    return render(request, 'comunidad/ver_tarea.html', {'tarea': tarea})










def ceder_rol_admin(request, comunidad_id, nuevo_admin_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    
    # Verificar si el usuario actual es el administrador
    if comunidad.administrador.user != request.user:
        return redirect('mi_comunidad', comunidad_id=comunidad_id)

    # Verificar que el nuevo administrador es un miembro de la comunidad
    nuevo_admin = get_object_or_404(User, id=nuevo_admin_id)
    if nuevo_admin not in comunidad.usuarios.all():
        return redirect('mi_comunidad', comunidad_id=comunidad_id)

    # Crear el registro de cambio de admin
    AdminCambio.objects.create(
        comunidad=comunidad,
        usuario_old=request.user,
        usuario_new=nuevo_admin,
        tipo='cesión'
    )

    # Actualizar el rol de administrador
    nuevo_admin_obj, _ = Administrador.objects.get_or_create(user=nuevo_admin)
    comunidad.administrador = nuevo_admin_obj
    comunidad.save()

    # Crear la notificación de cambio de administrador
    NotificacionSalida.objects.create(
        usuario=request.user,
        comunidad=comunidad,
        mensaje=f'El administrador {request.user.username} ha cedido su rol a {nuevo_admin.username}.'
    )

    return redirect('mi_comunidad', comunidad_id=comunidad_id)









def eliminar_usuario(request, comunidad_id, usuario_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    usuario = get_object_or_404(User, id=usuario_id)

    # Verificar si el usuario actual es el administrador
    if comunidad.administrador.user != request.user:
        return redirect('mi_comunidad', comunidad_id=comunidad_id)

    # Eliminar al usuario de la comunidad
    comunidad.usuarios.remove(usuario)

    # Registrar la expulsión
    Expulsion.objects.create(
        admin=comunidad.administrador,
        usuario=usuario,
        comunidad=comunidad
    )

    # Notificar al usuario expulsado si lo deseas
    messages.success(request, f'{usuario.username} ha sido expulsado de la comunidad.')
    
    return redirect('mi_comunidad', comunidad_id=comunidad_id)












def salir_comunidad(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)

    # Si quien sale es el admin, elegimos nuevo admin y registramos el cambio
    if comunidad.administrador.user == request.user:
        otros = list(comunidad.usuarios.exclude(id=request.user.id))
        if otros:
            nuevo_user = otros[0]
            # Crear un registro de cambio de administrador
            AdminCambio.objects.create(
                comunidad=comunidad,
                usuario_old=request.user,
                usuario_new=nuevo_user,
                tipo='abandono'
            )
            # Asignar nuevo Administrador
            nuevo_admin, _ = Administrador.objects.get_or_create(user=nuevo_user)
            comunidad.administrador = nuevo_admin
            comunidad.save()
            # Crear la notificación de salida
            NotificacionSalida.objects.create(
                usuario=request.user,
                comunidad=comunidad,
                mensaje=f'El administrador {request.user.username} ha abandonado la comunidad; nuevo administrador: {nuevo_user.username}'
            )
        else:
            # Sin más usuarios, eliminar la comunidad
            comunidad.delete()
            return redirect('comunidad')  # Redirigir a la lista de comunidades

    # Para los usuarios normales, solo se registran las salidas
    comunidad.usuarios.remove(request.user)
    NotificacionSalida.objects.create(
        usuario=request.user,
        comunidad=comunidad,
        mensaje=f'{request.user.username} ha abandonado la comunidad'
    )

    # Verificar si la comunidad está vacía
    if not comunidad.usuarios.exists():
        comunidad.delete()

    return redirect('comunidad')





def finalizar_tarea(request, tarea_id):
    tarea = get_object_or_404(Publicacion, id=tarea_id, realizada_por=request.user)
    # notificar al dueño
    NotificacionSalida.objects.create(
        usuario=tarea.usuario,       
        comunidad=tarea.comunidad,
        mensaje=(
          f'{request.user.username} ha finalizado tu tarea: '
          f'{tarea.categoria.nombre} – {tarea.descripcion[:30]}'
        )
    )
    tarea.delete()
    return redirect('mis_tareas')



def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Publicacion, id=tarea_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('ver_tarea', tarea_id=tarea.id)  # Redirigir a la vista de detalles
    else:
        form = PublicacionForm(instance=tarea)

    return render(request, 'comunidad/editar_tarea.html', {'form': form, 'tarea': tarea})
