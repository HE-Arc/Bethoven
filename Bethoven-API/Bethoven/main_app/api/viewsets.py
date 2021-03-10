
from rest_framework import viewsets ,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from main_app.models import *


class BethovenUserViewSet(viewsets.ModelViewSet):
    queryset = BethovenUser.objects.all()
    serializer_class =  BethovenUserSerializers 

class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

    permission_classes = [permissions.AllowAny]

    def create(self,request):
        print(request.user)
        serializer = CreateBetSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            bet = serializer.save()
            #bet.owner = request.user.BethovenUser
            #bet.save()
            return Response({
                "Bet" : BetSerializer(bet).data,
                "message": "Bet Created Successfully."
            })
    def update(self,request):
        return Response({
            "message" : "A envoyer"
        })

    