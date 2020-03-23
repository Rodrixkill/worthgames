from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

# Create your models here.
fs = FileSystemStorage(location='worthgames/static/images/')


class Juego(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('title', max_length=200)
    puntuacion=models.FloatField('puntuacion')
    descripcion=models.TextField('descripcion')
    linksGameplay= models.TextField('links')
    image=models.ImageField(storage=fs)
    created=models.ForeignKey(get_user_model(),on_delete=models.PROTECT)
    votantes=models.TextField('votantes',blank=True,default='')
    aceptado = models.BooleanField(default=False)

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    juego = models.ForeignKey(Juego, null=False, blank=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE)
    contenido = models.TextField('Contenido')

class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    comentario = models.ForeignKey(Comentario, null=False, blank=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE)
    contenido = models.TextField('Contenido')
