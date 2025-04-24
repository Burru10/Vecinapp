from django.urls import path
from .views import comunidad, crear_comunidad, mi_comunidad, realizar_tarea, salir_comunidad, buscar_comunidades, solicitar_union_ajax

urlpatterns = [
    path('', comunidad, name="comunidad"),
    path('crear/', crear_comunidad, name="crear_comunidad"),
    path('<int:comunidad_id>/', mi_comunidad, name="mi_comunidad"),
    path('realizar_tarea/<int:tarea_id>/', realizar_tarea, name='realizar_tarea'),
    path('salir/<int:comunidad_id>/', salir_comunidad, name='salir_comunidad'),
    path('buscar/', buscar_comunidades, name='buscar_comunidades'),
    path('solicitar-union/ajax/<int:comunidad_id>/', solicitar_union_ajax, name='solicitar_union_ajax'),

]