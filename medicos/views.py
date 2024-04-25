from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from .models import Especialidade, DadosMedico, is_medico


def cadastro(request):
  if is_medico(request.user):
    messages.add_message(request, constants.WARNING, 'Você já é médico')
    return redirect('/medicos/abrir-horarios/')
  
  if request.method == 'GET':
    especialidades = Especialidade.objects.all()

    return render(request, 'cadastro_medico.html', {'especialidades': especialidades, 'is_medico': is_medico(request.user)}) # contexts
  elif request.method == 'POST':
    crm = request.POST.get('crm')
    cim = request.FILES.get('cim')
    nome = request.POST.get('nome')
    cep = request.POST.get('cep')
    rua = request.POST.get('rua')
    bairro = request.POST.get('bairro')
    numero = request.POST.get('numero')
    rg = request.FILES.get('rg')
    foto = request.FILES.get('foto')
    especialidade = request.POST.get('especialidade')
    descricao = request.POST.get('descricao')
    valor_consulta = request.POST.get('valor_consulta')

    dados_medico = DadosMedico(
      crm=crm,
      cedula_identidade_medica=cim,
      nome=nome,
      cep=cep,
      rua=rua,
      bairro=bairro,
      numero=numero,
      rg=rg,
      foto=foto,
      especialidade_id=especialidade,
      descricao=descricao,
      valor_consulta=valor_consulta,
      user=request.user
    )
    dados_medico.save()

    messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso')
    return redirect('/medicos/abrir-horarios/')