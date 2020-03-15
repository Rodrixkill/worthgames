from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request,'game.html')

def gameplay(request,game_id):
    return render(request,'Gameplays.html')

def comentario(request,game_id):
    return render(request,'Comentarios.html')

