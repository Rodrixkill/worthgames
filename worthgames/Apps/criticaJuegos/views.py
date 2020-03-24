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
from django.db.models import Case, When, Value, IntegerField


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
                                puntuacion=10, votantes='+5')
            juegoCreate.save()
            return redirect('allgames')

    return render(request, 'formGame.html')


@login_required
def game(request,game_id):
    if request.POST:
        if request.POST['voto']=='+':
            usuario=request.POST['usuarioid']
            juego=request.POST['id']
            game = Juego.objects.get(pk=juego)
            listaDeVotantes=game.votantes.split(",")
            pos="+"+str(usuario)
            neg="-"+str(usuario)
            votantesNuevo=""
            if pos in listaDeVotantes:
                print("correcto")
                votantesNuevo=game.votantes
            elif neg in listaDeVotantes:
                for i in listaDeVotantes:
                    if i==neg:
                        votantesNuevo=votantesNuevo+","+pos
                    else:
                        votantesNuevo=votantesNuevo+","+i
            else:
                votantesNuevo=game.votantes+",+"+str(usuario)
            listaNueva=votantesNuevo.split(",")
            positivos=0
            negativos=0
            count=len(listaNueva)
            for i in listaNueva:
                if len(i)<1:
                    count-=1
                elif i[0]=="+":
                    positivos+=1
                elif i[0]=="-":
                    negativos+=1
            puntuacionCambiada=0
            if count>1:
                puntuacionCambiada=round((positivos*10) / count,1)
            nuevaPuntuacion= Juego.objects.filter(pk=juego).update(puntuacion=puntuacionCambiada)
            game = Juego.objects.filter(pk=juego).update(votantes=votantesNuevo)
        elif request.POST['voto']=='-':
            usuario=request.POST['usuarioid']
            juego=request.POST['id']
            game = Juego.objects.get(pk=juego)
            listaDeVotantes=game.votantes.split(",")
            pos="+"+str(usuario)
            neg="-"+str(usuario)
            votantesNuevo=""
            if pos in listaDeVotantes:
                for i in listaDeVotantes:
                    if i==pos:
                        votantesNuevo=votantesNuevo+","+neg
                    else:
                        votantesNuevo=votantesNuevo+","+i
            elif neg in listaDeVotantes:
                votantesNuevo=game.votantes
            else:
                votantesNuevo=game.votantes+",-"+str(usuario)
            listaNueva=votantesNuevo.split(",")
            positivos=0
            negativos=0
            count=len(listaNueva)
            print(listaNueva)
            for i in listaNueva:
                if len(i)<1:
                    count-=1
                elif i[0]=="+":
                    positivos+=1
                elif i[0]=="-":
                    negativos+=1
            puntuacionCambiada=0
            if count>1:
                puntuacionCambiada=round((positivos*10) / count,1)
            nuevaPuntuacion= Juego.objects.filter(pk=juego).update(puntuacion=puntuacionCambiada)
            game = Juego.objects.filter(pk=juego).update(votantes=votantesNuevo)
    obj = Juego.objects.get(pk=game_id)
    numeroDeVotantes = obj.votantes.count('-') + obj.votantes.count('+')
    return render(request,'game2.html',{'game': obj , 'cant':numeroDeVotantes})

@login_required
def gameplay(request,game_id):
    obj = Juego.objects.get(pk=game_id)
    string = obj.linksGameplay.split(',')
    return render(request,'Gameplays.html',{'game': obj,'links':string })

@login_required
def deleteG(request,game_id):
    result="No existe solicitud"
    if request.POST:
        if request.POST['type']=='game':
            val=request.POST['val']
            delete=Juego.objects.get(pk=val).delete()
            result="Juego eliminado con exito"
        elif request.POST['type']=='coment':
            val=request.POST['val']
            delete=Comentario.objects.get(pk=val).delete()
            result="Comentario eliminado con exito"
        elif request.POST['type']=='respuesta':
            val=request.POST['val']
            delete=Respuesta.objects.get(pk=val).delete()
            result="Respuesta eliminado con exito"
        else:
            result="datos enviados incorrectos"
    return render(request,'errors.html',{'error':result})


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

    if request.POST:
        order= request.POST['order_by']
        if order == "puntuacion":
            games = Juego.objects.all().order_by('-puntuacion')    
        elif order == "votos":
            games = sorted(Juego.objects.all(), key=lambda n: -len(n.votantes.split(",")))  
    
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




