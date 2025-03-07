from django.urls import path
from Web import views

urlpatterns = [
    path('', views.index, name="index"),
    path('servicios', views.servicios, name="servicios"),
    path('comunidad', views.comunidad, name="comunidad"),
    path('sobre_nosotros', views.sobre_nosotros, name="sobre_nosotros"),
]