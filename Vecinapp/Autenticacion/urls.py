from django.urls import path

from .views import  Cerrar_sesion, user_login, registro

urlpatterns = [
    #path('', VRegistro.as_view(), name='autenticacion'),
    path('registro', registro, name='autenticacion'),
    path('cerrar_sesion', Cerrar_sesion, name='cerrar_sesion'),
    path('login', user_login, name='login'),
]