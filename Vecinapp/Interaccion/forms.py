from django import forms
from .models import Mensaje

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe un mensaje...',
                'autocomplete': 'off'
            })
        }
