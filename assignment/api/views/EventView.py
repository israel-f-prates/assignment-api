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
            # By returning 422 instead of a less descriptive code, I could be
            # leaking too much information to the client (i.e.: a user could
            # infer the balance by trial and error).
            return Response(0, status.HTTP_422_UNPROCESSABLE_ENTITY)
        origin.save()
        origin_serializer = AccountSerializer(origin)
        withdraw_serializer = WithdrawSerializer({ 'origin' : origin_serializer.data })
        return Response(withdraw_serializer.data, status.HTTP_201_CREATED)

    # Since this operation relies on first withdrawing and then depositing,
    # it is not suited for actual use, because it is prone to racing conditions
    # or could leave an inconsistent state in the event that the application
    # fails in-between the operations.
    #
    # Since I don't know on which platform this code would run, I cannot blindly
    # rely on a serialization mechanism (for example: if this would be served as
    # a multiprocess app, I would need an OS semaphore, but the implementation
    # differs depending on the platform; if it were multithreaded, then I could
    # rely on the facilities provided by Python alone).
    #
    # On the other hand, I could delegate the serialization to the database by
    # creating a stored procedure that uses atomic transactions, but I won't go
    # down this route for two reasons:
    #   1. This is a sample app and should be kept simple.
    #   2. The database technology I'm using is far from adequate to be used
    #      for such purposes.
    def transfer(self, origin_id, destination_id, amount):
        try:
            origin = Account.objects.get(id=origin_id)
        except Account.DoesNotExist:
            return Response(0, status.HTTP_404_NOT_FOUND)
        try:
            origin.withdraw(amount)
        except ValueError:
            # Same as earlier comment about HTTP 422.
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
