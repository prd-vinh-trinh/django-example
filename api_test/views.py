from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse

# Create your views here.
class TestAPIView(viewsets.ModelViewSet):
    
    def list(self,request,*args,**kwangs):
        # return Response("My response here!")
        return JsonResponse({'message':'API response here'},status = 200)