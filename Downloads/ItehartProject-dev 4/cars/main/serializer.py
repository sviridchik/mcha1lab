from .models import *

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password  # Register serializer




class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    class Meta:
         model = Profile
         fields = [ 'date_of_birth', 'email', 'dtp_times','username','password']

    def save(self, **kwargs):
        user = User.objects.create_user(self.data['username'], self.data['email'], self.data['password'])
        profile = Profile.objects.create(user=user, date_of_birth=self.data['date_of_birth'],
                               email=self.data['email'],
                               dtp_times=self.data['dtp_times'],)
        return profile
