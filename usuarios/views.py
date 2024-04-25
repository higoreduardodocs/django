from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth


def cadastro(request):
  # print(request.META)
  # return HttpResponse('Hello world')
  if request.method == 'GET':
    return render(request, 'cadastro.html')
  elif request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')

    users = User.objects.filter(username=username)

    if users.exists():
      messages.add_message(request, constants.ERROR, 'Usuário já cadastrado')
      return redirect('/usuarios/cadastro/')
    
    users = User.objects.filter(email=email)

    if users.exists():
      messages.add_message(request, constants.ERROR, 'Email já cadastrado')
      return redirect('/usuarios/cadastro/')

    if senha != confirmar_senha:
      messages.add_message(request, constants.ERROR, 'Senha e confirmar senha devem ser iguais')
      return redirect('/usuarios/cadastro/')
    
    if len(senha) < 6:
      messages.add_message(request, constants.ERROR, 'Senha deve ter mais de 6 caracteres')
      return redirect('/usuarios/cadastro/')
    
    User.objects.create_user(
      username=username,
      email=email,
      password=senha
    )
    messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
    return redirect('/usuarios/login/')

def login(request):
  if request.method == 'GET':
    return render(request, 'login.html')
  elif request.method == 'POST':
    username = request.POST.get('username')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=username, password=senha)

    if user:
      auth.login(request, user)
      return redirect('/pacientes/home/')
    
    messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
    return redirect('/usuarios/login/')

def logout(request):
  if request.user:
    auth.logout(request)

  return redirect('/usuarios/login/')