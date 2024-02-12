from api.models.Account import Account
from api.serializers.AccountSerializer import AccountSerializer
from api.serializers.DepositSerializer import DepositSerializer
from api.serializers.EventSerializer import EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class EventView(APIView):
    def deposit(self, destination, amount):
        account, created = Account.objects.get_or_create(id=destination)
        account.deposit(amount)
        account.save()
        account_serializer = AccountSerializer(account)
        deposit_serializer = DepositSerializer({ 'destination' : account_serializer.data })
        return Response(deposit_serializer.data, status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def withdraw(self, request):
        try:
            account = Account.objects.get(id=request.data['origin'])
        except Account.DoesNotExist:
            return Response(0, status.HTTP_404_NOT_FOUND)
        account.withdraw(request.data['amount'])
        account.save()
        data = { 'origin' : AccountSerializer(account).data }
        return Response(data, status.HTTP_200_OK)

    def transfer(self, request):
        try:
            origin = Account.objects.get(account_id=request.data['origin'])
        except Account.DoesNotExist:
            return Response(0, status.HTTP_404_NOT_FOUND)
        origin.withdraw(request.data['amount'])
        origin.save()
        destination, created = Account.objects.get_or_create(account_id=request.data['destination'])
        destination.deposit(request.data['amount'])
        destination.save()
        data = {
            'origin' : AccountSerializer(origin).data,
            'destination' : AccountSerializer(destination).data
        }
        return Response(data, status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def post(self, request):
        event = EventSerializer(data=request.data)
        if not event.is_valid():
            return Response(0, status.HTTP_400_BAD_REQUEST)
        if event.validated_data.get('type') == 'deposit':
            return self.deposit(
                destination=event.validated_data.get('destination'),
                amount=event.validated_data.get('amount')
            )
        elif event.validated_data.get('type') == 'withdraw':
            return self.withdraw(
                origin=event.validated_data.get('origin'),
                amount=event.validated_data.get('amount')
            )
        elif event.validated_data.get('type') == 'transfer':
            return self.transfer(
                origin=event.validated_data.get('origin'),
                destination=event.validated_data.get('destination'),
                amount=event.validated_data.get('amount')
            )
        else:
            return Response(0, status.HTTP_404_NOT_FOUND)
