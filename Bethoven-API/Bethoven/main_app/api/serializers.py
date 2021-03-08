from rest_framework import serializers 
from main_app.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        return BethovenUser.create_bethoven_user(username,email,password)
        #return error

class BethovenUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BethovenUser
        fields = ['coins', 'user']