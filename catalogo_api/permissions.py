from rest_framework import permissions

class IsGerente(permissions.BasePermission):
    #Permissão personalizada para permitir que apenas o Gerente tenha acesso ao CRUD completo
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_perfil == 'Gerente'