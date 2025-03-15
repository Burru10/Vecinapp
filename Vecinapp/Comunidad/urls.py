from django.urls import path
from Comunidad import views

urlpatterns = [
    path('', views.comunidad, name="comunidad"),
]