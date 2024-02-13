from .AccountSerializer import AccountSerializer
from rest_framework import serializers

class DepositSerializer(serializers.Serializer):
    destination = AccountSerializer()

    class Meta():
        fields = '__all__'
