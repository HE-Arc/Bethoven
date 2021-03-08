from rest_framework import serializers 
from main_app.models import *


class BethovenUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = BethovenUser
        fields = ['user']

class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password1 = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password1 = validated_data['password1']
        password2 = validated_data['password2']
        if(password1 == password2):
            bethovenUser = BethovenUser.create_bethoven_user(username,email,password1)
            return bethovenUser
        #return error
    
