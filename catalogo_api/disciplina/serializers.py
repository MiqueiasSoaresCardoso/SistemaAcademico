from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from .models import Curso
from .models import Disciplina

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

    def validate(self, data):
        curso_id = data.get('curso')
        nova_carga_horaria = data.get('carga_horaria')

        if not curso_id:
            raise serializers.ValidationError("O campo 'curso' é obrigatório!")

        try:
            curso = Curso.objects.get(id=curso_id.id)
        except Curso.DoesNotExist:
            raise serializers.ValidationError("O curso selecionado não existe.")

        # Regra: não adicionar disciplina a curso inativado
        if not curso.ativo_curso:
            raise serializers.ValidationError(
                "Não é possível associar a disciplina a este curso, pois ele está inativo.")

        soma_cargas_horarias = curso.disciplinas.aggregate(
            total=Coalesce(Sum('carga_horaria'), 0)
        )['total']

        # Considera a carga horária da disciplina que está sendo atualizada
        if self.instance:
            soma_cargas_horarias -= self.instance.carga_horaria

        # Regra: a soma das cargas horárias não pode ultrapassar a carga horária total
        if soma_cargas_horarias + nova_carga_horaria > curso.carga_horaria:
            raise serializers.ValidationError(
                f"A soma das cargas horárias ({soma_cargas_horarias + nova_carga_horaria}) "
                f"ultrapassa a carga horária total do curso ({curso.carga_horaria})."
            )

        return data

    def validate_codigo_disciplina(self, value):
        if Disciplina.objects.filter(codigo_disciplina=value, ativo_disciplina=True).exists():
            raise serializers.ValidationError("Já existe uma disciplina ativa com este código.")
        return value