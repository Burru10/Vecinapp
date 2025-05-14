from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import localtime
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Mensaje
from Comunidad.models import Comunidad, SolicitudUnion, Publicacion, SalidaUnion, Expulsion, AdminCambio, NotificacionSalida
from .forms import MensajeForm


def bandeja_mensajes(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    usuarios = comunidad.usuarios.exclude(id=request.user.id)

    datos_usuarios = []

    for u in usuarios:
        mensajes = Mensaje.objects.filter(
            Q(remitente=request.user, destinatario=u) |
            Q(remitente=u, destinatario=request.user)
        ).order_by('-fecha_envio')

        ultimo = mensajes.first()
        no_leidos = mensajes.filter(destinatario=request.user, remitente=u, leido=False).count()

        datos_usuarios.append({
            'usuario': u,
            'ultimo_mensaje': ultimo.contenido if ultimo else '',
            'hora': localtime(ultimo.fecha_envio).strftime('%H:%M') if ultimo else '',
            'fecha_obj': ultimo.fecha_envio if ultimo else None,
            'no_leidos': no_leidos
        })

    # Ordenar por fecha (usuarios sin mensajes van al final)
    datos_usuarios.sort(
        key=lambda x: x['fecha_obj'] or timezone.make_aware(timezone.datetime.min),
        reverse=True
    )

    return render(request, 'interaccion/bandeja.html', {
        'datos_usuarios': datos_usuarios,
        'comunidad': comunidad
    })


def actualizar_bandeja(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    usuarios = comunidad.usuarios.exclude(id=request.user.id)

    datos_usuarios = []

    for u in usuarios:
        mensajes = Mensaje.objects.filter(
            Q(remitente=request.user, destinatario=u) |
            Q(remitente=u, destinatario=request.user)
        ).order_by('-fecha_envio')

        ultimo = mensajes.first()
        no_leidos = mensajes.filter(destinatario=request.user, remitente=u, leido=False).count()

        datos_usuarios.append({
            'usuario': u,
            'ultimo_mensaje': ultimo.contenido if ultimo else '',
            'hora': localtime(ultimo.fecha_envio).strftime('%H:%M') if ultimo else '',
            'fecha_obj': ultimo.fecha_envio if ultimo else None,
            'no_leidos': no_leidos
        })

    datos_usuarios.sort(
        key=lambda x: x['fecha_obj'] or timezone.make_aware(timezone.datetime.min),
        reverse=True
    )

    html = render_to_string('interaccion/bandeja_ajax.html', {
        'datos_usuarios': datos_usuarios,
        'comunidad': comunidad
    })
    return JsonResponse({'html': html})


def conversacion(request, comunidad_id, usuario_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id, usuarios=request.user)
    otro_usuario = get_object_or_404(User, id=usuario_id)

    mensajes = Mensaje.objects.filter(
        Q(remitente=request.user, destinatario=otro_usuario) |
        Q(remitente=otro_usuario, destinatario=request.user)
    ).order_by('fecha_envio')

    # Marcar como leídos antes de todo
    mensajes.filter(destinatario=request.user, leido=False).update(leido=True)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.destinatario = otro_usuario
            mensaje.save()
            return JsonResponse({'success': True})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('interaccion/mensajes_ajax.html', {
            'mensajes': mensajes,
            'request': request
        })
        return JsonResponse({'html': html})

    form = MensajeForm()

    return render(request, 'interaccion/chat.html', {
        'mensajes': mensajes,
        'form': form,
        'otro_usuario': otro_usuario,
        'comunidad': comunidad
    })


#Vistas para las notificaciones

def notificaciones_admin(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id, administrador__user=request.user)
    solicitudes = SolicitudUnion.objects.filter(comunidad=comunidad, aceptada=None)
    return render(request, 'interaccion/notificaciones_admin.html', {
        'solicitudes': solicitudes,
        'comunidad': comunidad,
    })

def notificaciones_usuario(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id, usuarios=request.user)
    notifications = []

    # 1) Has ingresado a la comunidad
    for j in SolicitudUnion.objects.filter(
        comunidad=comunidad,
        usuario=request.user,
        aceptada=True
    ):
        # Marcar como leído
        j.visto_usuario = True
        j.save()

        notifications.append({
            'fecha': j.fecha,
            'texto': f'Has ingresado a la comunidad {comunidad.nombre}',
            'visto_usuario': j.visto_usuario
        })

    # 2) Tarea aceptada
    for t in Publicacion.objects.filter(
        comunidad=comunidad,
        usuario=request.user,
        realizada_por__isnull=False
    ):
        notifications.append({
            'fecha': t.fecha_publicacion,
            'texto': (
                f'{t.realizada_por.username} ha aceptado tu tarea: '
                f'{t.categoria.nombre} – {t.descripcion[:30]}'
            ),
            'visto_usuario': True  # Asumimos que se ve la notificación cuando se marca
        })

    # 3) Tarea finalizada
    for t in Publicacion.objects.filter(
        comunidad=comunidad,
        usuario=request.user,
        estado='completada',
        realizada_por__isnull=False
    ):
        notifications.append({
            'fecha': t.fecha_publicacion,
            'texto': (
                f'{t.realizada_por.username} ha finalizado tu tarea: '
                f'{t.categoria.nombre} – {t.descripcion[:30]}'
            ),
            'visto_usuario': True
        })

    # 4) Notificaciones de salida
    for s in NotificacionSalida.objects.filter(comunidad=comunidad, usuario=request.user):
        notifications.append({
            'fecha': s.fecha,
            'texto': s.mensaje,
            'visto_usuario': True
        })

    # 5) Expulsión de usuario
    for e in Expulsion.objects.filter(comunidad=comunidad):
        notifications.append({
            'fecha': e.fecha,
            'texto': f'{e.admin.user.username} ha expulsado a {e.usuario.username}',
            'visto_usuario': True
        })

    # Ordenar por fecha descendente
    notifications.sort(key=lambda x: x['fecha'], reverse=True)

    return render(request, 'interaccion/notificaciones_usuario.html', {
        'comunidad': comunidad,
        'notifications': notifications,
    })



def gestionar_solicitud(request, solicitud_id, decision):
    solicitud = get_object_or_404(SolicitudUnion, id=solicitud_id)

    if solicitud.comunidad.administrador.user != request.user:
        return redirect('notificaciones_admin')

    if decision == "aceptar":
        solicitud.aceptada = True
        solicitud.comunidad.usuarios.add(solicitud.usuario)
    elif decision == "rechazar":
        solicitud.aceptada = False

    solicitud.save()
    return redirect('notificaciones_admin', solicitud.comunidad.id)