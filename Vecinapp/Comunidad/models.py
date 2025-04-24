from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from enum import Enum

class EstadoPublicacion(Enum):
    ABIERTA = 'abierta'
    EN_PROGRESO = 'en progreso'
    COMPLETADA = 'completada'

    @classmethod
    def choices(cls):
        return [(estado.value, estado.name.replace("_", " ").title()) for estado in cls]


class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='administrador')

    def __str__(self):
        return self.user.username
    

class Comunidad(models.Model):
    nombre = models.CharField(max_length=255)
    provincia = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    usuarios = models.ManyToManyField(User, related_name='comunidades')
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='comunidades')

    def __str__(self):
        return self.nombre


class CategoriaTarea(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'CategoriaTarea'
        verbose_name_plural = 'CategoriasTareas'

    def __str__(self):
        return self.nombre
    
    
class Publicacion(models.Model):
    categoria = models.ForeignKey(CategoriaTarea, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=2000, blank=False)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    realizada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_realizadas')
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, related_name='publicaciones')
    estado = models.CharField(
        max_length=20, 
        choices=EstadoPublicacion.choices(), 
        default=EstadoPublicacion.ABIERTA.value
    )

    def __str__(self):
        return str(self.categoria)
    

class SolicitudUnion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    aceptada = models.BooleanField(null=True, blank=True)  # None = pendiente
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Pendiente" if self.aceptada is None else ("Aceptada" if self.aceptada else "Rechazada")
        return f"{self.usuario.username} → {self.comunidad.nombre} ({estado})"
