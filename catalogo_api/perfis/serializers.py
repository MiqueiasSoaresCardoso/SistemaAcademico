from .models import Perfil
from rest_framework import serializers

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'codigo_perfil', 'tipo_perfil', 'email','senha','ativo_perfil']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        #fazendo Hash da senha
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


