from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')
@login_required
def form(request):
    return render(request,'FormGame.html')

@login_required
def game(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    return render(request,'game2.html',{'game': obj })

@login_required
def gameplay(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    string = obj.linksGameplay.split(',')
    return render(request,'Gameplays.html',{'game': obj,'links':string })

@login_required
def comentario(request,game_id):
    if request.POST:
        juegoid= request.POST['gameID']
        if request.POST['resp']=='true':
            user = request.POST['userID']
            comentid= request.POST['comentID']
            ukey =Usuario.objects.get(id=user)
            ckey =Comentario.objects.get(id=comentid)
            comen= request.POST['coment']
            respuestaC= Respuesta(comentario=ckey,usuario=ukey,contenido=comen)
            respuestaC.save()
        else:
            user = request.POST['userID']
            comentid= request.POST['gameID']
            ukey =Usuario.objects.get(id=user)
            jkey =Juego.objects.get(id=comentid)
            comen= request.POST['coment']
            comentarioCreate= Comentario(juego=jkey,usuario=ukey,contenido=comen)
            comentarioCreate.save()
        return HttpResponseRedirect("/comentario/"+juegoid+"/")
    obj = Juego.objects.get(pk=game_id)
    comentarios = Comentario.objects.filter(juego = game_id).values('id')
    names = Comentario.objects.filter(juego = game_id).values('usuario')
    conexion=[]
    usernames=[]
    for i in comentarios:
        nombre=i['id']
        respuestas=Respuesta.objects.filter(comentario = nombre)
        #usuarios=Usuario.objects.filter(id=nomb).values('Nombre')
        conexion.append((i['id'],respuestas))
    coments = Comentario.objects.filter(juego = game_id)
    return render(request,'Comentarios.html',{'game':obj,'conexion':conexion,'comentarios':coments})

@login_required
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




