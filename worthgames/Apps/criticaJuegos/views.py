from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
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
    string = obj.linksGameplay.split(',')
    return render(request,'Gameplays.html',{'game': obj,'links':string })

def comentario(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    comentarios = Comentario.objects.filter(juego = game_id).values('id')
    names = Comentario.objects.filter(juego = game_id).values('usuario')
    conexion=[]
    usernames=[]
    for i in comentarios:
        nombre=i['id']
        respuestas=Respuesta.objects.filter(comentario = nombre)
        print(respuestas)
        #usuarios=Usuario.objects.filter(id=nomb).values('Nombre')
        conexion.append((i['id'],respuestas))
    print(conexion[0][0])
    coments = Comentario.objects.filter(juego = game_id)
    return render(request,'Comentarios.html',{'game':obj,'conexion':conexion,'comentarios':coments})

def allgames(request):
    games = list()
    query = ""
    search=""
    if request.GET:
        query = request.GET['q']
        search = str(query)
    if search == "":
        games = Juego.objects.all()
    else:
        games = search1(search)
        
    return render(request,'game.html', {'games' : games,'query':query})

def search1(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Juego.objects.filter(
                Q(title__icontains=q)
            ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))




