from django.shortcuts import render, redirect
from .models import Especialidade, DadosMedico, DatasAbertas, is_medico
from pacientes.models import Consulta, Documento
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime, timedelta


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
  
def horarios(request):
  if not is_medico(request.user):
    messages.add_message(request, constants.WARNING, 'Somente médicos podem abrir horários')
    return redirect('/usuarios/logout')
  
  if request.method == 'GET':
    dados_medico = DadosMedico.objects.get(user=request.user)
    data_abertas = DatasAbertas.objects.filter(user=request.user)
    
    return render(request, 'abrir_horarios.html', {'dados_medico': dados_medico, 'data_abertas': data_abertas, 'is_medico': is_medico(request.user)})
  elif request.method == 'POST':
    data = request.POST.get('data')
    data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')

    if data_formatada <= datetime.now():
      messages.add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual')
      return redirect('/medicos/abrir-horarios/')
    
    data_aberta = DatasAbertas(
      data=data_formatada,
      user=request.user
    )
    data_aberta.save()

    messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso')
    return redirect('/medicos/abrir-horarios/')
  
def consultas_medico(request):
  if not is_medico(request.user):
    messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página')
    return redirect('/usuarios/logout')
  
  hoje = datetime.now().date()
  amanha = hoje + timedelta(days=1)

  consultas_hoje = Consulta.objects.filter(data_agendada__user=request.user).filter(data_agendada__data__gte=hoje).filter(data_agendada__data__lt=amanha)
  consultas_restantes = Consulta.objects.filter(data_agendada__user=request.user).exclude(id__in=consultas_hoje.values('id'))

  return render(request, 'consultas_medico.html', {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes, 'is_medico': is_medico(request.user)})

def consulta_area_medico(request, id_consulta):
  if not is_medico(request.user):
    messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página')
    return redirect('/usuarios/logout')
  
  if request.method == 'GET':
    consulta = Consulta.objects.get(id=id_consulta)
    documentos = Documento.objects.filter(consulta=consulta)
    return render(request, 'consulta_area_medico.html', {'consulta': consulta, 'documentos': documentos, 'is_medico': is_medico(request.user)})
  elif request.method == 'POST':
    consulta = Consulta.objects.get(id=id_consulta)
    link = request.POST.get('link')

    if consulta.status == 'C':
      messages.add_message(request, constants.WARNING, 'Essa consulta já foi cancelada, você não pode inicia-la')
      return redirect(f'/medicos/consulta-area-medico/{id_consulta}')
    elif consulta.status == 'F':
      messages.add_message(request, constants.WARNING, 'Essa consulta já foi finalizada, você não pode inicia-la')
      return redirect(f'/medicos/consulta-area-medico/{id_consulta}')
    
    consulta.link = link
    consulta.status = 'I'
    consulta.save()

    messages.add_message(request, constants.SUCCESS, 'Consulta inicializada com sucesso')
    return redirect(f'/medicos/consulta-area-medico/{id_consulta}')

def finalizar_consulta(request, id_consulta):
  if not is_medico(request.user):
    messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página')
    return redirect('/usuarios/logout')

  consulta = Consulta.objects.get(id=id_consulta)

  if request.user != consulta.data_agendada.user:
    messages.add_message(request, constants.ERROR, 'Está consulta não é sua')
    return redirect('/medicos/consultas-medico/')

  consulta.status = 'F'
  consulta.save()
  return redirect(f'/medicos/consulta-area-medico/{id_consulta}')

def adicionar_documento(request, id_consulta):
  if not is_medico(request.user):
    messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página')
    return redirect('/usuarios/logout')
  
  consulta = Consulta.objects.get(id=id_consulta)

  if request.user != consulta.data_agendada.user:
    messages.add_message(request, constants.ERROR, 'Está consulta não é sua')
    return redirect('/medicos/consultas-medico/')
  
  if request.method == 'POST':
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')

    if not documento:
      messages.add_message(request, constants.WARNING, 'Adicione o documento.')
      return redirect(f'/medicos/consulta-area-medico/{id_consulta}')
  
    documento = Documento(
      consulta=consulta,
      titulo=titulo,
      documento=documento
    )
    documento.save()
    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso')
    return redirect(f'/medicos/consulta-area-medico/{id_consulta}')
