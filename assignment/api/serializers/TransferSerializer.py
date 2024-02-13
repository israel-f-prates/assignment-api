from .AccountSerializer import AccountSerializer
from rest_framework import serializers

class TransferSerializer(serializers.Serializer):
    destination = AccountSerializer()
    origin = AccountSerializer()

    class Meta():
        fields = '__all__'
