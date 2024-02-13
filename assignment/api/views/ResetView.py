from api.models.Account import Account
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse

class ResetView(APIView):
    def post(self, request):
        Account.objects.all().delete()
        return HttpResponse('OK', status=status.HTTP_200_OK)
