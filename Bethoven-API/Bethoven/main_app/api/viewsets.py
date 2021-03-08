
from rest_framework import viewsets 
from .serializers import *
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.
    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    #Bethovenuser for this viewset
    queryset = BethovenUser.objects.all()
    serializer_class = BethovenUserSerializer

    #define permissions
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {'create': [AllowAny],
                                #'list': [IsAuthenticated], etc
                                }

    def create(self, request):
        """Register a new user"""
        #special serializer : this time, we use the 'user' one
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            bethovenUser = serializer.save()
            return Response({
                "user": BethovenUserSerializer(bethovenUser).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })

    def destroy(self, request, *args, **kwargs):
        """
        Little redefinition to verify destroy integrity :
            * The request user is the one that is to be deleted
            * The user is to be deleted with the bethovenUser
        """
        bethovenUserToDelete = self.get_object()
        if(request.user.id != bethovenUserToDelete.user.id):
            logger.error(f"User {request.user}[{request.user.id}] tried to delete user {bethovenUserToDelete}[{bethovenUserToDelete.user.id}]")
            raise serializers.ValidationError("You must be the user to delete !")
        bethovenUserToDelete.user.delete() #felte on cascade anyway
        return Response({"message": "User deleted succesfully",})
        
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]