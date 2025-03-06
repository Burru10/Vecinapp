from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provincia = models.CharField(max_length=255)
    localidad = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=10)
    direccion = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username