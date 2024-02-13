from .AccountSerializer import AccountSerializer
from rest_framework import serializers

class WithdrawSerializer(serializers.Serializer):
    origin = AccountSerializer()

    class Meta():
        fields = '__all__'
