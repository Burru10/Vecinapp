from django.urls import path
from .views import comunidad, crear_comunidad, mi_comunidad, realizar_tarea, salir_comunidad, buscar_comunidades, solicitar_union_ajax, mis_tareas, ver_tarea, eliminar_usuario, ceder_rol_admin, finalizar_tarea, editar_tarea

urlpatterns = [
    path('', comunidad, name="comunidad"),
    path('crear/', crear_comunidad, name="crear_comunidad"),
    path('<int:comunidad_id>/', mi_comunidad, name="mi_comunidad"),
    path('realizar_tarea/<int:tarea_id>/', realizar_tarea, name='realizar_tarea'),
    path('salir/<int:comunidad_id>/', salir_comunidad, name='salir_comunidad'),
    path('buscar/', buscar_comunidades, name='buscar_comunidades'),
    path('solicitar-union/ajax/<int:comunidad_id>/', solicitar_union_ajax, name='solicitar_union_ajax'),
    path('mis_tareas/', mis_tareas, name='mis_tareas'),
    path('ver_tarea/<int:tarea_id>/', ver_tarea, name='ver_tarea'),
    path('comunidad/<int:comunidad_id>/ceder_admin/<int:nuevo_admin_id>/', ceder_rol_admin, name='ceder_rol_admin'),
    path('comunidad/<int:comunidad_id>/eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('finalizar_tarea/<int:tarea_id>/', finalizar_tarea, name='finalizar_tarea'),
    path('editar_tarea/<int:tarea_id>/', editar_tarea, name='editar_tarea'),
]