from django.shortcuts import render
from django.http import HttpResponse


def cadastro(request):
  # print(request.META)
  # return HttpResponse('Hello world')
  if request.method == 'GET':
    return render(request, 'cadastro.html')

def login(request):
  if request.method == 'GET':
    return render(request, 'login.html')