from rest_framework import viewsets
from .models import Curso
from .serializers import CursoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated]

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
