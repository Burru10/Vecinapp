from django import forms

class FormularioContacto(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, required=True)

    email = forms.EmailField(label="Email", required=True)

    mensaje = forms.CharField(label="Mensaje", widget=forms.Textarea, required=True)