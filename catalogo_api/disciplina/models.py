import uuid

from django.db import models

from catalogo_api.curso.models import Curso


# Create your models here.

class Disciplina(models.Model):
    id_disciplina = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_disciplina = models.CharField(max_length=10,blank=False, null=False)
    nome_curso = models.CharField(max_length=120,blank=False, null=False)
    carga_horaria = models.IntegerField(blank=False, null=False)
    curso = models.ForeignKey(Curso,on_delete=models.SET_NULL,null=True, related_name='disciplinas')
    ativo_disciplina = models.BooleanField(default=True)
    def __str__(self):
        return self.codigo_curso
