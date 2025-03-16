from django.db import models

# Create your models here.
from django.contrib.auth.models import User

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
    
