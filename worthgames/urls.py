"""worthgames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from worthgames.Apps.criticaJuegos import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/<game_id>/',views.game,name='game'),
    path('gameplay/<game_id>/',views.gameplay,name='gameplay'),
    path('comentario/<game_id>/',views.comentario,name='comentario'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('form/',views.form,name='form'),
    path('allgames/',views.allgames,name='allgames'),
    path('accounts/', include('django.contrib.auth.urls')),

]
