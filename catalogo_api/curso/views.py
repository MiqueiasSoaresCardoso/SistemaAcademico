from rest_framework import viewsets
from .models import Curso
from .serializers import CursoSerializer
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action

from ..permissions import IsGerente


# Create your views here.
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsGerente]

    def get_permissions(self):
        if self.action == 'create':
            return [IsGerente()]
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsGerente()]

    # endpoints personalizados para ativação/inativação
    @action(detail=True, methods=['put', 'patch'])
    def inativar(self, request, pk=None):
        disciplina = Curso.get_object()
        disciplina.ativo_disciplina = False
        disciplina.save()
        return Response({'Disciplina': disciplina + 'inativada com sucesso'})

    @action(detail=True, methods=['put', 'patch'])
    def ativar(self, request, pk=None):
        disciplina = Curso.get_object()
        disciplina.ativo_disciplina = True
        disciplina.save()
        return Response({'Disciplina': disciplina + 'ativada com sucesso'})
