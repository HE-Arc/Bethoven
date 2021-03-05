from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from .api.serializers import *
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .models import *
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


   
   
########### register here #####################################  
class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bethovenUser = serializer.save()
        return Response({
            "user": BethovenUserSerializers(bethovenUser,context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
    
class Coucou(generics.GenericAPIView):
    def get(self, request, *args,  **kwargs):
        return Response({
            "message": "Coucou.  Now perform Login to get your token",
        })
   