from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from .api.serializers import *
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .models import *

class ServerState(generics.GenericAPIView):
    def get(self, request, *args,  **kwargs):
        return Response({
            "message": "Server is running...",
        })