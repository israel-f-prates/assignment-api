from api.models.Account import Account
from api.serializers.AccountSerializer import AccountSerializer
from api.serializers.DepositSerializer import DepositSerializer
from api.serializers.EventSerializer import EventSerializer
from api.serializers.TransferSerializer import TransferSerializer
from api.serializers.WithdrawSerializer import WithdrawSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class EventView(APIView):
    def deposit(self, destination_id, amount):
        destination, _ = Account.objects.get_or_create(id=destination_id)
        try:
            destination.deposit(amount)
        except ValueError:
            return Response(0, status.HTTP_422_UNPROCESSABLE_ENTITY)
        destination.save()
        destination_serializer = AccountSerializer(destination)
        deposit_serializer = DepositSerializer({ 'destination' : destination_serializer.data })
        return Response(deposit_serializer.data, status.HTTP_201_CREATED)

    def withdraw(self, origin_id, amount):
        try:
            origin = Account.objects.get(id=origin_id)
        except Account.DoesNotExist:
            return Response(0, status.HTTP_404_NOT_FOUND)
        try:
            origin.withdraw(amount)
        except ValueError:
            return Response(0, status.HTTP_422_UNPROCESSABLE_ENTITY)
        origin.save()
        origin_serializer = AccountSerializer(origin)
        withdraw_serializer = WithdrawSerializer({ 'origin' : origin_serializer.data })
        return Response(withdraw_serializer.data, status.HTTP_201_CREATED)

    def transfer(self, origin_id, destination_id, amount):
        try:
            origin = Account.objects.get(id=origin_id)
        except Account.DoesNotExist:
            return Response(0, status.HTTP_404_NOT_FOUND)
        try:
            origin.withdraw(amount)
        except ValueError:
            return Response(0, status.HTTP_422_UNPROCESSABLE_ENTITY)
        origin.save()
        destination, _ = Account.objects.get_or_create(id=destination_id)
        try:
            destination.deposit(amount)
        except ValueError:
            return Response(0, status.HTTP_422_UNPROCESSABLE_ENTITY)
        destination.save()
        origin_serializer = AccountSerializer(origin)
        destination_serializer = AccountSerializer(destination)
        transfer_serializer = TransferSerializer({
            'origin' : origin_serializer.data,
            'destination' : destination_serializer.data
        })
        return Response(transfer_serializer.data, status.HTTP_201_CREATED)

    def post(self, request):
        event = EventSerializer(data=request.data)
        if not event.is_valid():
            return Response(0, status.HTTP_400_BAD_REQUEST)
        if event.validated_data.get('type') == 'deposit':
            return self.deposit(
                destination_id=event.validated_data.get('destination'),
                amount=event.validated_data.get('amount')
            )
        elif event.validated_data.get('type') == 'withdraw':
            return self.withdraw(
                origin_id=event.validated_data.get('origin'),
                amount=event.validated_data.get('amount')
            )
        elif event.validated_data.get('type') == 'transfer':
            return self.transfer(
                origin_id=event.validated_data.get('origin'),
                destination_id=event.validated_data.get('destination'),
                amount=event.validated_data.get('amount')
            )
        else:
            return Response(0, status.HTTP_404_NOT_FOUND)
