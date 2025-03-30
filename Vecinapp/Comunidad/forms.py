from django import forms
from .models import Comunidad, CategoriaTarea, Publicacion

class ComunidadForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ["nombre", "provincia", "localidad", "codigo_postal", "direccion", "numero"]


class PublicacionForm(forms.ModelForm):
    
    categoria = forms.ModelChoiceField(
        queryset=CategoriaTarea.objects.all(),
        empty_label="Seleccione una categoría",
        label="Categoría"
    )
    class Meta:
        model = Publicacion
        fields = ["categoria", "descripcion"]