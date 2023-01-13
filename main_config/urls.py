"""main_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('leave/', views.sair, name='sair'),
    path('registro/', views.registro, name='registro' ),
    path('divulgar/', views.divulgar, name='divulgar'),
    path('adotar/', views.adotar, name='adotar'),
    path('meuspets/', views.meuspets, name='Meus_Pets' ),
    path('excluir/<int:id>', views.excluir_pet , name='excluir_pet'),
    path('ver_pet/<int:id>', views.ver_pet, name="ver_pet"),
    path('pedido_adocao/<int:id_pet>', views.pedido_adocao, name="pedido_adocao"),
    path('ver_pedido_adocao/', views.ver_pedido_adocao, name="ver_pedido_adocao"),
    path('processa_pedido_adocao/<int:id_pedido>', views.processa_pedido_adocao, name="processa_pedido_adocao"),

]
