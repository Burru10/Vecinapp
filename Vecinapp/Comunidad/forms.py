from django import forms
from .models import Comunidad, CategoriaTarea, Publicacion

class ComunidadForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ["nombre", "provincia", "localidad", "codigo_postal", "direccion", "numero"]


# forms.py
class PublicacionForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=CategoriaTarea.objects.all(),
        empty_label="Seleccione una categoría",
        label="Categoría",
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg'
        })
    )

    class Meta:
        model = Publicacion
        fields = ["categoria", "descripcion"]
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada de la tarea',
                'style': 'height: 150px;'
            })
        }



