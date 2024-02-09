from rest_framework import serializers
from api.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [ 'account_id', 'balance' ]
