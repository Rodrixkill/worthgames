from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def form(request):
    return render(request,'FormGame.html')

def game(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    return render(request,'game2.html',{'game': obj })

def gameplay(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    return render(request,'Gameplays.html',{'game': obj })

def comentario(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    comentarios = Comentario.objects.filter(juego = game_id).values('id')
    conexion=[]
    for i in comentarios:
        nombre=i['id']
        respuestas=Respuesta.objects.filter(comentario = nombre)
        conexion.append((i['id'],respuestas))

    coments = Comentario.objects.filter(juego = game_id)
    return render(request,'Comentarios.html',{'game':obj,'conexion':conexion,'comentarios':coments})

def allgames(request):
    games = Juego.objects.all()
    return render(request,'game.html', {'games' : games})

