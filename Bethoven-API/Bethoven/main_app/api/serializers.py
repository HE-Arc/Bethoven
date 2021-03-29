from rest_framework import serializers 
from main_app.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

###     USER SERIALIZERS    ###
class UserRegisterSerializer(serializers.ModelSerializer):
    """Register serializer that helps to register a new user (uses the auth.user model)"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """Create an empty bethovenuser along this auth.user, link them together (uses model function)"""
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
        fields = ['coins', 'id', 'username', 'email','following']

class BethovenUpdateSerializer(serializers.ModelSerializer):
    """Bethoven serializer that also fetches the username,email from the auth.user"""
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    #Not mandatory to change the password at every update, still a possibility
    new_password = serializers.CharField(required=False, default=None)

    class Meta:
        model = BethovenUser
        fields = ['username', 'email', 'password', 'new_password']

    def update(self, instance, validated_data):
        """ Updating a user requires that the password fits the old one to change the data. """
        if not instance.user.check_password(validated_data["password"]) :
            raise serializers.ValidationError("Your password must be the same")

        user = instance.user
        user.email = validated_data["email"]
        user.username = validated_data["username"]
        if validated_data["new_password"]:
            user.password = validated_data["new_password"]
        user.save()
        return instance.user
        
class BethovenProfileCard(serializers.ModelSerializer):
    """A sanitized representation of the user available to everyone"""
    username = serializers.CharField(source='user.username')
    class Meta:
        model = BethovenUser
        fields = ['username', 'coins', 'id']


###     BET SERIALIZERS    ###

class BetSerializer(serializers.ModelSerializer):
    currentUserBet = serializers.SerializerMethodField()
    class Meta:
        model = Bet
        fields = ('id', 'title', 'description', 'choice0', 'choice1', 'isClosed', 'result', 'bet_ratio', 'currentUserBet')

    def get_currentUserBet(self, obj):
        try:
            currentUser = self.context['request'].user.bethovenUser
        except Exception:
            return None

        try:
            userbet = UserBet.objects.get(user=currentUser, bet=obj)
            return {
                "amount" : userbet.amount, 
                "choice" : userbet.choice,
            }
        except Exception:
            return None

class CreateBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('title', 'description', 'choice0', 'choice1')

class PartialUpdateBetSerializer(serializers.ModelSerializer):
    isClosed = serializers.BooleanField(required=False,default=None)
    result = serializers.IntegerField(required=False,default=None)
    class Meta:
        model = Bet
        fields = ('isClosed','result')
    
    def update(self, instance, validated_data):

        if validated_data["isClosed"]:
            closed = validated_data["isClosed"]
            if not instance.isClosed and closed :
                instance.isClosed = closed
                instance.save()
            return instance
        if validated_data["result"]:
            result = validated_data["result"]
            if((result == 1 or result == 0) and  instance.result is None and instance.isClosed):
                instance.result = result
                instance.save()
                instance.give()
            return instance

class UserBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBet
        fields = ('user','amount', 'choice','bet')
        
class GambleUserBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBet
        fields = ('amount', 'choice')
        
 ###     FEED SERIALIZERS    ###
class FeedSerializer(serializers.Serializer):
    """ Verifies the info on a trending request  """
    number = serializers.IntegerField(min_value=1) #number is required - how much bet is this feed's lenght
    order = serializers.ChoiceField(choices=[("hot", False), ("trending",True)], required=False, default=True)
    betFrom = serializers.PrimaryKeyRelatedField(queryset=Bet.objects.all(), required=False, default=None)