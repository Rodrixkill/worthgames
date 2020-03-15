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

