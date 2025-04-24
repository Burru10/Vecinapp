from django.urls import path
from .views import bandeja_mensajes, conversacion, actualizar_bandeja, notificaciones_admin, notificaciones_usuario, gestionar_solicitud

urlpatterns = [
    path('mensajes/<int:comunidad_id>/', bandeja_mensajes, name='mensajes'),

    path('chat/<int:usuario_id>/', conversacion, name='conversacion'),

    path('bandeja-ajax/<int:comunidad_id>/', actualizar_bandeja, name='actualizar_bandeja'),

    path('notificaciones/admin/', notificaciones_admin, name='notificaciones_admin'),
    path('notificaciones/usuario/', notificaciones_usuario, name='notificaciones_usuario'),
    path('solicitud/<int:solicitud_id>/<str:decision>/', gestionar_solicitud, name='gestionar_solicitud'),
]
