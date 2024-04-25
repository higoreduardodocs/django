from django.db import models
from django.contrib.auth.models import User
from medicos.models import DatasAbertas


class Consulta(models.Model):
  status_choice = (
    ('A', 'Agendado'),
    ('F', 'Finalizado'),
    ('C', 'Cancelada'),
    ('I', 'Iniciada'),
  )
  paciente=models.ForeignKey(User, on_delete=models.DO_NOTHING)
  data_agendada=models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
  status=models.CharField(max_length=1, choices=status_choice, default='A')
  link=models.URLField(null=True, blank=True)

  def __str__(self):
    return self.paciente.username
