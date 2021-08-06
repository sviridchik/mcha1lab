from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView, CreateAPIView

from .serializer import UserSerializer, Profile


@api_view(['GET'])
def change(request):
    user = request.user
    if user.is_authenticated:
        return Response({}, status=status.HTTP_200_OK)
    else:
        raise PermissionDenied()

def change_red(request):
    return redirect("/health")

def signin(request):
    # print(request.get_host(),request.get_port())
    s = "http://"+request.get_host()+"/auth/jwt/create"
    # raise Exception("http://"+request.get_host()+"/auth/jwt/create")
    return redirect(s)
    # return redirect("http://127.0.0.1:8000/auth/jwt/create")


class SignUp(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]




# @api_view(['POST']) сеньюкью
# def signup(request):
#     serializer =
#     if serializer.is_valid():
#         raise Exception('OK')
#     else:
#         return Response({'Error', serializer.errors})