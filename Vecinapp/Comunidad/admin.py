from django.contrib import admin

# Register your models here.
from .models import Administrador, Comunidad, Publicacion, CategoriaTarea

class Comunidades(admin.ModelAdmin):
    list_display = ('nombre', 'provincia', 'localidad','direccion')

class Publicaciones(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'fecha_publicacion','comunidad', 'estado')
    list_filter = ('comunidad',)

admin.site.register(Administrador)
admin.site.register(Comunidad, Comunidades)
admin.site.register(Publicacion, Publicaciones)
admin.site.register(CategoriaTarea)
