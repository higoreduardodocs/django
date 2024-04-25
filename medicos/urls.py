from django.urls import path
from . import views


urlpatterns = [
  path('cadastro-medico/', views.cadastro, name='cadastro-medico'),
  path('abrir-horarios/', views.horarios, name='abrir-horarios'),
  path('consultas-medico/', views.consultas_medico, name='consultas-medico'),
]