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
    UserViewSet : Viewset that manages the user : register, CRUD...
    Login is managed by Oauth2, not by this viewset.
    """
    #Model for this viewset
    queryset = BethovenUser.objects.all()
    serializer_class = BethovenUserSerializer

    #define permissions - default to "isselfuser" as the sensible data should not be accessed by someone else
    permission_classes = [isSelfUser]
    permission_classes_by_action = {
                                    'create': [AllowAny], #allow anyone to register
                                    'list': [IsAdminUser], #restrict the "list" view that contains the email and should not be accessible to all people
                                }

    def create(self, request):
        """Register a new user"""
        #special serializer : The 'user' one handles the user data
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "user": BethovenUserSerializer(user).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })

    def destroy(self, request, *args, **kwargs):
        """
        The Destroy function should not only destroy the bethoven user, but also the linked Auth.User.
        As the delete is on cascade, deleting the user is enough to delete the bethoven user.
        """
        bethovenUser = self.get_object()
        bethovenUser.user.delete()
        return Response({"success":1, "message": "User deleted succesfully",})

    def update(self, request, *args, **kwargs):
        """The update method uses the updateserilalizer that verifies the password is the good one before applying any change"""
        serializer = BethovenUpdateSerializer(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({"success":1, "message": "User updated succesfully",})

    def get_permissions(self):
        """Function that allow for defining permissions by function"""
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]