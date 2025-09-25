from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.response import Response
from catalogo_api.perfis.models import Perfil
from catalogo_api.perfis.serializers import PerfilSerializer
from catalogo_api.permissions import IsGerente


# Create your views here.
class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsGerente()]
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsGerente()]

    #endpoints personalizados para ativação/inativação
    @action(detail=True,methods=['put','patch'])
    def inativar(self, request, pk=None):
        perfil = self.get_object()
        perfil.ativo_perfil = False
        perfil.save()
        return Response({'Perfil': perfil.email + 'inativado com sucesso!'})

    @action(detail=True,methods=['put','patch'])
    def ativar(self, request, pk=None):
        perfil = self.get_object()
        perfil.ativo_perfil = True
        perfil.save()
        return Response({'Perfil': perfil.email + 'inativado com sucesso!'})
