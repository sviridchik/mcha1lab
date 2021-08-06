from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status


# Create your views here.
@api_view(['GET'])
def change(request):
    return Response({}, status=status.HTTP_200_OK)
