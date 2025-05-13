from django.contrib import admin

# Register your models here.
from .models import Administrador, Comunidad, Publicacion, CategoriaTarea, SolicitudUnion, SalidaUnion, AdminCambio, NotificacionSalida

class SolicitudUnionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comunidad', 'aceptada', 'fecha', 'visto_usuario')
    list_filter = ('aceptada', 'fecha')
    search_fields = ('usuario__username', 'comunidad__nombre')
    list_editable = ('aceptada', 'visto_usuario')

class SalidaUnionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comunidad', 'fecha')
    search_fields = ('usuario__username', 'comunidad__nombre')
    list_filter = ('fecha',)

class ExpulsionAdmin(admin.ModelAdmin):
    list_display = ('admin', 'usuario', 'comunidad', 'fecha')
    search_fields = ('admin__user__username', 'usuario__username', 'comunidad__nombre')
    list_filter = ('fecha',)

class AdminCambioAdmin(admin.ModelAdmin):
    list_display = ('comunidad', 'usuario_old', 'usuario_new', 'tipo', 'fecha')
    search_fields = ('comunidad__nombre', 'usuario_old__username', 'usuario_new__username')
    list_filter = ('tipo', 'fecha')

admin.site.register(SolicitudUnion, SolicitudUnionAdmin)
admin.site.register(SalidaUnion, SalidaUnionAdmin)
admin.site.register(NotificacionSalida)
admin.site.register(AdminCambio, AdminCambioAdmin)

class Comunidades(admin.ModelAdmin):
    list_display = ('nombre', 'provincia', 'localidad','direccion')

class Publicaciones(admin.ModelAdmin):
    list_display = ('usuario', 'categoria', 'fecha_publicacion','comunidad', 'estado')
    list_filter = ('comunidad',)

admin.site.register(Administrador)
admin.site.register(Comunidad, Comunidades)
admin.site.register(Publicacion, Publicaciones)
admin.site.register(CategoriaTarea)
