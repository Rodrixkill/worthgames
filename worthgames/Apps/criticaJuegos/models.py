from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
fs = FileSystemStorage(location='worthgames/media/photos/')

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField('Nombre', max_length=200)
    password = models.TextField('Password')
    correo =models.EmailField('Correo', max_length=100)
    contacto = models.CharField('contacto', max_length=200)
    admin = models.BooleanField('Admin', default=False)

class Juego(models.Model):
    id = models.AutoField(primary_key=True)
    puntuacion=models.PositiveIntegerField('puntuacion')
    descripcion=models.TextField('descripcion')
    linksGameplay= models.TextField('links')
    image=models.ImageField(storage=fs)
    created=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    votantes=models.TextField('votantes')

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    juego = models.ForeignKey(Juego, null=False, blank=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)
    contenido = models.TextField('Contenido')

class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    comentario = models.ForeignKey(Comentario, null=False, blank=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)
    contenido = models.TextField('Contenido')