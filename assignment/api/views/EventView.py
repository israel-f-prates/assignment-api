from api.models.Account import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class EventView(APIView):
    def post(self, request):
        if request.data['type'] == 'deposit':
            account, created = Account.objects.get_or_create(account_id=request.data['destination'])
            account.deposit(request.data['amount'])
            account.save()
            response = Response(account.balance, status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        elif request.data['type'] == 'withdraw':
            try:
                account = Account.objects.get(account_id=request.data['origin'])
                account.withdraw(request.data['amount'])
                account.save()
                response = Response(account.balance, status.HTTP_200_OK)
            except Account.DoesNotExist:
                response = Response(0, status.HTTP_404_NOT_FOUND)
        elif request.data['type'] == 'transfer':
            try:
                origin = Account.objects.get(account_id=request.data['origin'])
                origin.withdraw(request.data['amount'])
                origin.save()
            except Account.DoesNotExist:
                return Response(0, status.HTTP_404_NOT_FOUND)
            destination, created = Account.objects.get_or_create(account_id=request.data['destination'])
            destination.deposit(request.data['amount'])
            destination.save()
            response = Response(0, status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        else:
            response = Response(0, status.HTTP_404_NOT_FOUND)
        return response
