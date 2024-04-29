from django.urls import path
from . import views


urlpatterns = [
  path('cadastro-medico/', views.cadastro, name='cadastro-medico'),
  path('abrir-horarios/', views.horarios, name='abrir-horarios'),
  path('consultas-medico/', views.consultas_medico, name='consultas-medico'),
  path('consulta-area-medico/<int:id_consulta>', views.consulta_area_medico, name='consulta-area-medico'),
  path('finalizar-consulta/<int:id_consulta>', views.finalizar_consulta, name='finalizar-consulta'),
  path('adicionar-documento/<int:id_consulta>', views.adicionar_documento, name='adicionar-documento'),
]