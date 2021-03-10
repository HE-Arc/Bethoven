
from main_app.api.viewsets import *
from rest_framework import routers 
  
router = routers.SimpleRouter() 
router.register(r'user', BethovenUserViewSet, basename ='user_api') 
router.register(r'bet',BetViewSet) 