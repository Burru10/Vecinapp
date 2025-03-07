from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

from django.contrib.auth import authenticate


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=30, required=True)
    last_name = forms.CharField(label="Apellidos", max_length=30, required=True)
    email = forms.EmailField(label="Correo electrónico", required=True)
    provincia = forms.CharField(label="Provincia", max_length=255, required=True)
    localidad = forms.CharField(label="Localidad", max_length=255, required=True)
    codigo_postal = forms.CharField(label="Código Postal", max_length=10, required=True)
    direccion = forms.CharField(label="Dirección", max_length=255, required=True)
    numero = forms.CharField(label="Número", max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 
                  'provincia', 'localidad', 'codigo_postal', 'direccion', 'numero',
                  'password1', 'password2']
    
    #Comprueba que no se registre un correo que ya está en uso
    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo ya está en uso")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                user=user, 
                provincia=self.cleaned_data['provincia'],
                localidad=self.cleaned_data['localidad'],
                codigo_postal=self.cleaned_data['codigo_postal'],
                direccion=self.cleaned_data['direccion'],
                numero=self.cleaned_data['numero']
            )
        return user
    


class FormularioLogin(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password and not authenticate(self.request, username=username, password=password):
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return super().clean()