from django.urls import path
from .views import comunidad, crear_comunidad

urlpatterns = [
    path('', comunidad, name="comunidad"),
    path('crear/', crear_comunidad, name="crear_comunidad"),
]