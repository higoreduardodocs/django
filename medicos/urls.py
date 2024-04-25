from django.urls import path
from . import views


urlpatterns = [
  path('cadastro-medico/', views.cadastro, name='cadastro-medico'),
]