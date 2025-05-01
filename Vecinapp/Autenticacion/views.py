from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegistroForm, FormularioLogin

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)

            # Crear contenido del correo
            subject = '¡Bienvenido a Vecinapp!'
            html_message = render_to_string('usuarios/correo_bienvenida.html', {'user': usuario})
            plain_message = strip_tags(html_message)
            to_email = usuario.email

            # Enviar el correo
            send_mail(subject, plain_message, None, [to_email], html_message=html_message)
            return redirect('index')
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "registro/registro.html", {"form": form})
    else:
        form = RegistroForm()

    return render(request, "registro/registro.html", {"form": form})

        
def Cerrar_sesion(request):
    logout(request)
    return redirect('index')

def user_login(request):
    if request.method == "POST":
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('comunidad')
    else:
        form = FormularioLogin()
    return render(request, "login/login.html", {"form": form})


#Impelementación de recuperar contraseña

class MiPasswordResetView(PasswordResetView):
    template_name = "recuperar_contra/password_reset_form.html"
    email_template_name = "recuperar_contra/password_reset_email.html"       # El cuerpo del correo
    subject_template_name = "recuperar_contra/password_reset_subject.txt"    # El asunto del correo
    success_url = reverse_lazy("password_reset_done")

class MiPasswordResetDoneView(PasswordResetDoneView):
    template_name = "recuperar_contra/password_reset_done.html"

class MiPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "recuperar_contra/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

class MiPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "recuperar_contra/password_reset_complete.html"


