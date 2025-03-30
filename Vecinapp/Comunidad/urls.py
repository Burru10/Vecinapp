from django.urls import path
from .views import comunidad, crear_comunidad, mi_comunidad, realizar_tarea

urlpatterns = [
    path('', comunidad, name="comunidad"),
    path('crear/', crear_comunidad, name="crear_comunidad"),
    path('<int:comunidad_id>/', mi_comunidad, name="mi_comunidad"),
    path('realizar_tarea/<int:tarea_id>/', realizar_tarea, name='realizar_tarea'),
]