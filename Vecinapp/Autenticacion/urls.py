from django.urls import path

from .views import  Cerrar_sesion, user_login, registro

from .views import MiPasswordResetView, MiPasswordResetDoneView, MiPasswordResetConfirmView, MiPasswordResetCompleteView

urlpatterns = [
    path('registro', registro, name='autenticacion'),
    path('cerrar_sesion', Cerrar_sesion, name='cerrar_sesion'),
    path('login', user_login, name='login'),
    path("password_reset/", MiPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", MiPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", MiPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", MiPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]