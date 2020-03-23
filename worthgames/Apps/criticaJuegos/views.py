from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .forms import RegisterFrom
from django.contrib.auth.models import User
from  django import forms


# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def register(request):
    if request.method == 'POST':
        form = RegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterFrom()
    return render(request, 'registration/register.html', {
        'form': form
    })

def login(request):
    return render(request,'registration/login.html')

@login_required
def form(request):
    if request.POST:
        user = request.POST['userID']
        titulo = request.POST['fname']
        link1 = request.POST['link1']
        links = 'https://www.youtube.com/embed/' + link1.split('=')[1]
        link2 = request.POST['link2']
        if(link2 != ''):
            links += ',https://www.youtube.com/embed/' + link2.split('=')[1]
        link3 = request.POST['link3']
        if (link3 != ''):
            links += ',https://www.youtube.com/embed/' + link3.split('=')[1]
        descrip  = request.POST['descrip']
        ukey = User.objects.get(id=user)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.cleaned_data['image']
            juegoCreate = Juego(title=titulo, descripcion=descrip, image=imagen, created=ukey, linksGameplay=links,
                                puntuacion=0, votantes=0)
            juegoCreate.save()
            return redirect('allgames')

    return render(request, 'formGame.html')


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
            ukey =User.objects.get(id=user)
            ckey =Comentario.objects.get(id=comentid)
            comen= request.POST['coment']
            respuestaC= Respuesta(comentario=ckey,usuario=ukey,contenido=comen)
            respuestaC.save()
        else:
            user = request.POST['userID']
            comentid= request.POST['gameID']
            ukey =User.objects.get(id=user)
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

@login_required
def acceptGame(request):
    if request.POST:
        if request.POST['accion'] == 'aceptar':
          juegoid = request.POST['gameID']
          juego = Juego.objects.get(pk=juegoid)
          juego.aceptado = 1
          juego.save()
        if request.POST['accion'] == 'borrar':
          juegoid = request.POST['gameID']
          juego = Juego.objects.get(pk=juegoid)
          juego.delete()

    games = Juego.objects.all()
    return render(request,'acceptGame.html',{'games': games })

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

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()




