from django.shortcuts import render, redirect
from .forms import FormularioContacto
from django.core.mail import EmailMessage
from django.contrib import messages

# Create your views here.

def contacto(request):
    formulario_contacto=FormularioContacto()

    if request.method == "POST":
        formulario_contacto=FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            mensaje = request.POST.get("mensaje")

            if email != request.user.email:
                messages.error(request, "El email no coincide con el del usuario")
                return render(request, "Contacto/contacto.html", {'formulario_contacto':formulario_contacto})

            email = EmailMessage("Nuevo mensaje de contacto - Vecinapp",
            "El usuario con nombre {} con la dirección de correo {} escribe lo siguiente:\n\n{}".format(nombre, email, mensaje),
            "", ["vecinappoficial@gmail.com"], reply_to=[email])

            try:
                email.send()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?novalido")


    return render(request, "Contacto/contacto.html", {'formulario_contacto':formulario_contacto})