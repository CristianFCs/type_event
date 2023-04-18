from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib import auth
import re

# Create your views here.

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
            return redirect(reverse('cadastro'))
        
        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, 'Senha muito fraca, insira no mínimo 8 caracteres e utilize ao menos uma letra')
            return redirect(reverse('cadastro'))
        
        if  not re.search(r'[a-zA-Z]', senha):
            messages.add_message(request, constants.ERROR, 'Insira ao menos uma letra em sua senha')
            return redirect(reverse('cadastro'))
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe.')
            return redirect(reverse('cadastro'))
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
        
        
        return redirect(reverse('login'))

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
    user = auth.authenticate(username=username, password=senha)
    
    if not user:
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return redirect(reverse('login'))
    
    auth.login(request, user)
    return redirect('/eventos/novo_evento/')
        