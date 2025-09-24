import uuid

from django.db import models

# Create your models here.

class Curso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_curso = models.CharField(max_length=10, unique=True)
    nome_curso = models.CharField(max_length=120)
    descricao_curso = models.TextField(blank=True, null=True)
    ativo_curso = models.BooleanField(default=True)
    carga_horaria = models.IntegerField(blank=False, null=False)
    def __str__(self):
        return self.codigo_curso