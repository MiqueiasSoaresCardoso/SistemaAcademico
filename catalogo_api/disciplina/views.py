import django_filters
from django.shortcuts import render
from rest_framework import viewsets,filters
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from permissions import IsGerente
from .serializers import DisciplinaSerializer
from .models import Disciplina
from rest_framework.response import Response
from rest_framework.decorators import action




# Create your views here.

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsGerente]
    #adicionando filtros
    filter_backends = [filters.SearchFilter,django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['ativo_disciplina','curso']
    search_fields = ['nome_disciplina','codigo_disciplina']

    def get_permissions(self):
        if self.action == 'create':
            return [IsGerente()]
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsGerente()]

    #endpoints personalizados para ativação/inativação
    @action(detail=True,methods=['put','patch'])
    def inativar(self,request, pk=None):
        disciplina = Disciplina.get_object()
        disciplina.ativo_disciplina = False
        disciplina.save()
        return Response({'Disciplina':disciplina + 'inativada com sucesso'})

    @action(detail=True, methods=['put', 'patch'])
    def ativar(self,request,pk=None):
        disciplina = Disciplina.get_object()
        disciplina.ativo_disciplina = True
        disciplina.save()
        return Response({'Disciplina': disciplina + 'ativada com sucesso'})