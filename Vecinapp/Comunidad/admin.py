from django.contrib import admin

# Register your models here.
from .models import Administrador, Comunidad

class Comunidades(admin.ModelAdmin):
    list_display = ('nombre', 'provincia', 'localidad','direccion')

admin.site.register(Administrador)
admin.site.register(Comunidad, Comunidades)