from api.models import Account
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BalanceView(APIView):
    filter_backends = [ SearchFilter ]
    search_fields = [ 'account_id' ]
    def get(self, request):
        if 'account_id' not in request.query_params:
            response = Response(0, status.HTTP_400_BAD_REQUEST)
        else:
            try:
                account = Account.objects.get(account_id=request.query_params.get('account_id'))
                response = Response(account.balance, status.HTTP_200_OK)
            except Account.DoesNotExist:
                response = Response(0, status.HTTP_404_NOT_FOUND)
        return response
