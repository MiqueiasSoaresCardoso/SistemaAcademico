

from catalogo_api.curso.models import Curso
from catalogo_api.disciplina import serializers


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

    def validate_codigo_curso(self, value):
        if Curso.objects.filter(codigo_curso=value, ativo=True).exists():
            raise serializers.ValidationError("Já existe um curso ativo com este código.")
        return value