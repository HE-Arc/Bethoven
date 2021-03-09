from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .custom_perm import isSelfUser

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

    #define permissions - default to "selfuser"
    permission_classes = [isSelfUser]
    permission_classes_by_action = {
                                    'create': [AllowAny],
                                    'list': [IsAdminUser],
                                }

    def create(self, request):
        """Register a new user"""
        #special serializer : The 'user' one handles the user data
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "user": BethovenUserSerializer(user).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })

    def destroy(self, request, *args, **kwargs):
        """
        Little redefinition to verify destroy integrity :
            * The request user is the one that is to be deleted
            * The user is to be deleted with the bethovenUser
        """
        bethovenUserToDelete = self.get_object()
        """if(request.user.id != bethovenUserToDelete.user.id):
            logger.error(f"User {request.user}[{request.user.id}] tried to delete user {bethovenUserToDelete}[{bethovenUserToDelete.user.id}]")
            raise serializers.ValidationError("You must be the user to delete !")"""
        bethovenUserToDelete.user.delete() #delete on cascade
        return Response({"success":1, "message": "User deleted succesfully",})

    def update(self, request, *args, **kwargs):
            serializer = BethovenUpdateSerializer(self.get_object(), data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response("User updated !")

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
            
    serializers_by_action = {
        'create' : UserSerializer,
        'update' : BethovenUpdateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializers_by_action[self.action]
        except KeyError: 
            #default
            return BethovenUserSerializer