from rest_framework import serializers

from ocorrencias.models import Ocorrencia


class OcorrenciaSerializer(serializers.ModelSerializer):

    class Meta:
        extra_args = {
            "is_active": {"read_only": True},
            "data": {"read_only": True},
            "status_flag": {"read_only": True},
        }
        model = Ocorrencia
        exclude = ["status_flag"]
