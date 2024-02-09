from api.models.Account import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ResetView(APIView):
    def post(self, request):
        Account.objects.all().delete()
        return Response(status=status.HTTP_200_OK)
