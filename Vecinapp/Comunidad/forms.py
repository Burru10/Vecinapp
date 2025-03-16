from django import forms
from .models import Comunidad

class ComunidadForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ["nombre", "provincia", "localidad", "codigo_postal", "direccion", "numero"]
