import decimal
from rest_framework import serializers

_valid_types = ('deposit', 'withdraw', 'transfer')

class EventSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=32)
    origin = serializers.CharField(max_length=128, default=None)
    destination = serializers.CharField(max_length=128, default=None)
    amount = serializers.DecimalField(max_digits=17, decimal_places=2)

    class Meta():
        fields = '__all__'

    def to_internal_value(self, data):
        if 'type' not in data:
            raise serializers.ValidationError
        if 'amount' not in data:
            raise serializers.ValidationError
        if data['type'] not in _valid_types:
            raise serializers.ValidationError
        try:
            decimal.Decimal(data['amount'])
        except decimal.ConversionSyntax:
            raise serializers.ValidationError
        return super().to_internal_value(data)