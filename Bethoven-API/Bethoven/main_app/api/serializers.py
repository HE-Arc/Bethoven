from rest_framework import serializers 
from main_app.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

##USER SERIALIZERS
class UserSerializer(serializers.ModelSerializer):
    """Register serializer that helps to register a new user (uses the auth.user model)"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """Create an empty bethovenuser along this auth.user, link them together (see model function)"""
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        return BethovenUser.create_bethoven_user(username,email,password)

class BethovenUserSerializer(serializers.ModelSerializer):
    """Bethoven serializer that also fetches the username,email from the auth.user"""
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = BethovenUser
        fields = ['coins', 'id', 'username', 'email']

class BethovenUpdateSerializer(serializers.ModelSerializer):
    """Bethoven serializer that also fetches the username,email from the auth.user"""
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    new_password = serializers.CharField(required=False, default=None)

    class Meta:
        model = BethovenUser
        fields = ['username', 'email', 'password', 'new_password']

    def update(self, instance, validated_data):
        if not instance.user.check_password(validated_data["password"]) :
            raise serializers.ValidationError("Your password must be the same")

        user = instance.user
        user.email = validated_data["email"]
        user.username = validated_data["username"]
        if validated_data["new_password"]:
            user.password = validated_data["new_password"]
        user.save()
        return instance.user