
from rest_framework import viewsets 
from .serializers import *

class BethovenUserViewSet(viewsets.ModelViewSet):
    queryset = BethovenUser.objects.all()
    serializer_class =  BethovenUserSerializers 