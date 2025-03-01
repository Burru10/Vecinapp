from django.urls import path
from Web import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contacto', views.contacto, name="contacto"),
    path('servicios', views.servicios, name="servicios"),
]