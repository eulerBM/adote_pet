from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from usuarios.models import *
from datetime import datetime
from django.core.mail import send_mail




def login_user (request):

    if request.method == 'GET':
        return render (request, 'login_user.html')

    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome, password=senha)

        if user is not None:
            login(request, user)
            return redirect('/home')

        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login_user.html')


def registro (request):

    if request.user.is_authenticated:
        return render (request, 'home.html')

    if request.method == 'GET':
        return render (request, 'register_user.html')
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_2 = request.POST.get('confirmar_senha')

        if senha != senha_2:
            messages.add_message(request, constants.ERROR, 'Senhas são diferentes')
            return render (request, 'register_user.html')

        try:
         
            user_register = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,

            )
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso, faça login!') 
            return render (request, 'login_user.html')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro do sistema, DESCULPE :(') 
            return render (request, 'login_user.html')


@login_required
def divulgar(request):

    if request.method == 'GET':
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return render(request, 'divulgar.html',{'tags':tags, 'racas':racas})
    
    elif request.method == 'POST':
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
        )

        pet.save()

        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)

        pet.save()
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        messages.add_message(request, constants.SUCCESS, 'Novo pet cadastrado')
        return render(request, 'adotar.html', {'tags': tags, 'racas': racas})





@login_required
def adotar(request):

    pets = Pet.objects.filter(status="P")
    racas = Raca.objects.all()

    if request.method == 'GET':

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if raca_filter == "10":
            all = Raca.objects.all()
            return render(request, 'adotar.html', {'pets': pets, 'racas': all, 'cidade': cidade, 'raca_filter': raca_filter})

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

 
        return render(request, 'adotar.html', {'pets': pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter})


@login_required
def meuspets(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(usuario=request.user)
        return render (request,'MeusPets.html', {'pets': pets})



@login_required
def excluir_pet (request, id):
    pet = Pet.objects.get(id=id)
    pet.delete()
    return redirect ('/meuspets/')


@login_required
def home (request):
    return render(request, 'home.html')

def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id=id)
        return render(request, 'ver_pet.html', {'pet': pet})


@login_required
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=request.user,
                          data=datetime.now())

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar/')


def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})


@login_required
def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    if status == "A":
        pedido.status = 'AP'
        string = '''Olá, sua adoção foi aprovada. ...'''
    elif status == "R":
        string = '''Olá, sua adoção foi recusada. ...'''
        pedido.status = 'R'

    pedido.save()

    
    print(pedido.usuario.email)
    email = send_mail(
        'Sua adoção foi processada',
        string,
        'caio@pythonando.com.br',
        [pedido.usuario.email,],
    )
    
    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado com sucesso')
    return redirect('ver_pedido_adocao')




















@login_required
def sair(request):
    logout(request)
    return redirect('/login/')

# Create your views here.
