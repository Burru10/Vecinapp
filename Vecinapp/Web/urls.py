from django.urls import path
from Web import views

urlpatterns = [
    path('', views.index, name="index"),
    path('servicios', views.servicios, name="servicios"),
    path('solicitudes', views.solicitudes, name="solicitudes"),
    path('sobre_nosotros', views.sobre_nosotros, name="sobre_nosotros"),
]