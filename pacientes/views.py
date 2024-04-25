from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from medicos.models import DadosMedico, Especialidade, DatasAbertas, is_medico
from .models import Consulta


def home(request):
  if request.method == 'GET':
    medicos = DadosMedico.objects.all()
    especialidades = Especialidade.objects.all()

    return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades, 'is_medico': is_medico(request.user)})

def escolher_horario(request, id_dados_medico):
  if request.method == 'GET':
    medico = DadosMedico.objects.get(id=id_dados_medico)
    datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gt=datetime.now()).filter(agendado=False)
    print(datas_abertas)

    return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})

def agendar_horario(request, id_agenda_aberta):
  if request.method == 'GET':
    data_aberta = DatasAbertas.objects.get(id=id_agenda_aberta)
    consulta = Consulta(
      paciente=request.user,
      data_agendada=data_aberta,
    )
    consulta.save()
    data_aberta.agendado = True
    data_aberta.save()

    messages.add_message(request, constants.SUCCESS, 'Consulta agendada com sucesso')
    return redirect('/pacientes/minhas-consultas/')
  
def minhas_consultas(request):
  if request.method == 'GET':
    # especialidades = request.GET.get('especialidades')
    data = request.GET.get('data')
    consultas = Consulta.objects.filter(paciente=request.user).filter(data_agendada__data__gte=datetime.now())

    if data:
      data_formatada = datetime.strptime(data, '%Y-%m-%d')
      if data_formatada <= datetime.now():
        consultas.filter(data_agendada__data__gte=data_formatada)

    return render(request, 'minhas_consultas.html', {'consultas': consultas, 'is_medico': is_medico(request.user)})
    
def consulta(request, id_consulta):
  if request.method == 'GET':
    consulta = Consulta.objects.get(id=id_consulta)
    if consulta.paciente != request.user:
      messages.add_message(request, constants.ERROR, 'Está consulta não é sua')
      return redirect('/paciente/minhas-consultas/')
    
    dado_medico = DadosMedico.objects.get(user=consulta.data_agendada.user)
    # documentos = Documento.objects.filter(consulta=consulta)

    return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico': dado_medico, 'documentos': [], 'is_medico': is_medico(request.user)})