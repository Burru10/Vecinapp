from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistroForm

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy


# Create your views here.

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('index')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        else:
            messages.error(request, "Información incorrecta")
    form = AuthenticationForm()
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


