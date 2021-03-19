from main_app.api.viewsets import *
from rest_framework import routers 
  
router = routers.SimpleRouter() 

router.register(r'users', UserViewSet, basename='users')
router.register(r'bets',BetViewSet, basename="bets") 