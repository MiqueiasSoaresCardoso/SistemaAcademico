from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import Disciplina
from rest_framework import serializers

from ..curso.models import Curso


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

    def validate(self, data):
        curso = data.get('curso')
        #carga_h da disciplina
        nova_carga_h = data.get('carga_horaria')

        if not curso:
            raise serializers.ValidationError("O campo 'curso' é obrigatório!" )

        #Agora eu preciso da soma das cargas horárias
        soma_carga_horaria = curso.disciplinas.aggregate(total=Coalesce(Sum('carga_horaria'),0))['total']

        #fazendo a soma da carga horária atual do curso, com a carga da nova disciplina inserida/atualizada
        if soma_carga_horaria + nova_carga_h > curso.carga_horaria:
            raise serializers.ValidationError(
                f"A soma das cargas horárias das disciplinas ({soma_carga_horaria + nova_carga_h}"
                f"ultrapassa a carga horária total do curso ({curso.carga_horaria})"
            )
        return data
