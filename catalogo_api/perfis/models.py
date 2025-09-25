import uuid
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Perfil(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_perfil = models.CharField(max_length=10, blank=False, null=False,unique=True)
    tipo_perfil = models.CharField(max_length=20, blank=False, null=False, choices=[('Discente',"Discente"),('Coordenador','Coordenador'),('Professor','Professor')])
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=10, blank=False, null=False)
    ativo_perfil = models.BooleanField(default=True)
    #era bom ter um nome
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tipo_perfil']

    #sobreescrever o metodo save(), para a implementação customizada e automatica do código do perfil
    def save(self, *args,**kwargs):
        if not self.codigo_perfil:
            ano_atual = date.today().year
            prefixo = f'MAT.{ano_atual}'

            #selecionando o código do ultimo perfil criado
            ultimo_perfil = Perfil.objects.filter(codigo_perfil__startswicth=prefixo).order_by('-codigo_perfil').first()

            if ultimo_perfil and ultimo_perfil.codigo_perfil:
                n_sequencial = int(ultimo_perfil.codigo_perfil.split('.')[-1]) + 1
            else:
                n_sequencial = 1

            self.codigo_perfil = f'{prefixo}.{n_sequencial}'

        super().save(*args,**kwargs)