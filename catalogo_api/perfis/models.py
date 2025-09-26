import uuid
from datetime import date

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class PerfilManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('ativo_perfil', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')
        return self.create_user(email,password,**extra_fields)

class Perfil(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_perfil = models.CharField(max_length=10, blank=False, null=False,unique=True)
    tipo_perfil = models.CharField(max_length=20, blank=False, null=False, choices=[('Discente',"Discente"),('Coordenador','Coordenador'),('Professor','Professor'),('Gerente','Gerente')])
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=10, blank=False, null=False)
    ativo_perfil = models.BooleanField(default=True)
    #era bom ter um nome
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tipo_perfil']

    objects = PerfilManager()

    #sobreescrever o metodo save(), para a implementação customizada e automatica do código do perfil
    def save(self, *args,**kwargs):
        if not self.codigo_perfil:
            ano_atual = date.today().year
            prefixo = f'MAT.{ano_atual}'

            #selecionando o código do ultimo perfil criado
            ultimo_perfil = Perfil.objects.filter(codigo_perfil__startswith=prefixo).order_by('-codigo_perfil').first()

            if ultimo_perfil and ultimo_perfil.codigo_perfil:
                n_sequencial = int(ultimo_perfil.codigo_perfil.split('.')[-1]) + 1
            else:
                n_sequencial = 1

            self.codigo_perfil = f'{prefixo}.{n_sequencial}'

        super().save(*args,**kwargs)