from rest_framework import viewsets, filters
import django_filters
from permissions import IsGerente
from .models import Curso
from .serializers import CursoSerializer
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
# Create your views here.
@extend_schema(tags=["Cursos"])
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsGerente]
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['ativo_curso', 'codigo_curso']
    search_fields = ['nome_curso', 'codigo_curso']

    def get_permissions(self):
        if self.action == 'create':
            return [IsGerente()]
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsGerente()]

    # endpoints personalizados para ativação/inativação
    @action(detail=True, methods=['put', 'patch'])
    def inativar(self, request, pk=None):
        curso = self.get_object()
        curso.ativo_curso = False
        curso.save()
        return Response({f'Curso: {curso} inativado com sucesso'})

    @action(detail=True, methods=['put', 'patch'])
    def ativar(self, request, pk=None):
        curso = self.get_object()
        curso.ativo_curso = True
        curso.save()
        return Response({f'Curso: {curso} ativado com sucesso'})
