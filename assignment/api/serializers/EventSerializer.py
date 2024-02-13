import decimal
from rest_framework import serializers

_valid_types = ('deposit', 'withdraw', 'transfer')
_destination_required = ('deposit', 'transfer')
_origin_required = ('withdraw', 'transfer')

class EventSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=32)
    origin = serializers.CharField(max_length=128, default=None)
    destination = serializers.CharField(max_length=128, default=None)
    amount = serializers.DecimalField(max_digits=17, decimal_places=2)

    class Meta():
        fields = '__all__'

    # The conversion between serialized and internal should handle validating
    # the event data, such as allowed types, amount range and so on, even
    # though the data may be validated again elsewhere in the code.
    def to_internal_value(self, data):
        if 'type' not in data:
            raise serializers.ValidationError
        if data['type'] not in _valid_types:
            raise serializers.ValidationError
        if data['type'] in _destination_required and 'destination' not in data:
            raise serializers.ValidationError
        if data['type'] in _origin_required and 'origin' not in data:
            raise serializers.ValidationError
        if 'amount' not in data:
            raise serializers.ValidationError
        try:
            amount = decimal.Decimal(data['amount'])
        except decimal.InvalidOperation:
            raise serializers.ValidationError
        if amount <= 0:
            raise serializers.ValidationError
        return super().to_internal_value(data)
