from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse

class CoffeeView(APIView):
    def get(self, request):
        return HttpResponse(0, status=status.HTTP_418_IM_A_TEAPOT)
