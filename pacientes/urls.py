from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('escolher-horario/<int:id_dados_medico>', views.escolher_horario, name='escolher-horario'),
  path('agendar-horario/<int:id_agenda_aberta>', views.agendar_horario, name='agendar-horario'),
  path('minhas-consultas/', views.minhas_consultas, name='minhas-consultas'),
  path('consulta/<int:id_consulta>', views.consulta, name='consulta'),
]