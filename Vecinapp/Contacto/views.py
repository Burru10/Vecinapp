from django.shortcuts import render, redirect
from .forms import FormularioContacto
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

# Create your views here.

def contacto(request):
    formulario_contacto=FormularioContacto()

    if request.method == "POST":
        formulario_contacto=FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = request.POST.get("nombre")
            email = request.user.email
            mensaje = request.POST.get("mensaje")

            email = EmailMessage("Mensaje desde la app de vecinapp",
            "El usuario con nombre {} con la dirección de correo {} escribe lo siguiente:\n\n{}".format(nombre, email, mensaje),
            request.user.email, ["vecinappoficial@gmail.com"], reply_to=[email])

            try:
                email.send()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?novalido")


    return render(request, "Contacto/contacto.html", {'formulario_contacto':formulario_contacto})