
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .custom_perm import isSelfUser , isBetOwner
import logging


logger = logging.getLogger(__name__)

class ViewsetFunctionPermissions(viewsets.ModelViewSet):
    """ 
    viewset thet allows to determine permissions by function :
        * Define permision_classes = [] as default permissions
        * Define permission_classes_by_action = { 'fct' : [permission], ... } as permission tailored for actions
    """
    class Meta:
        abstract = True

    def get_permissions(self):
        """Function that allow for defining permissions by function"""
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class UserViewSet(ViewsetFunctionPermissions):
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
                                    'retrieve': [AllowAny], #allow anyone to acess a profile
                                    'search': [AllowAny], #Allow anyone to search users
                                    'list': [IsAdminUser], #restrict the "list" view that contains the email and should not be accessible to all people
                                    'follow': [IsAuthenticated],  #follow/unfollow mecanism
                                    'unfollow': [IsAuthenticated],
                                    'me': [IsAuthenticated], #settings : Must be authenticated, will find user by its access token
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

    def retrieve(self, request, pk):
        """
        The detail view returns a user profile :
         * User card
         * User that this user follows
         * statistics of this user
         * The last 5 bets of this user
        """
        #fetch user
        user = BethovenUser.objects.get(pk=pk)
        #from user model : fetch profile, followed profile and last bets
        userProfileSerializer = BethovenProfileCard(user)
        followersProfilesSerializers = BethovenProfileCard(user.following, many=True)   #uses serializers with many=true to get
        lastBetsSerializer = BetSerializer(user.last_bets(5), many=True)                #a standardized list of profiles and bets
        return Response({
            "user" : userProfileSerializer.data,
            "follows" : followersProfilesSerializers.data,
            "statistics" : user.get_statistics(),
            "last bets" : lastBetsSerializer.data,
        })

    @action(detail=False)
    def me(self, request):   
        """ 
        The "me" endpoint allow users to access their personnal settings (username, email, id, etc...) by providing their access token. 
        Usefull to retrieve personnal informations (Except password, which is not sent).
        """
        user = request.user.bethovenUser
        serializer = BethovenUserSerializer(user)
        return Response(serializer.data)   

    @action(detail=True)
    def follow(self, request, pk):
        """
        Make a user follow another user - takes care that :
            * The user is not itself
            * The user is not currently followed by the requesting user
        """
        userToFollow = self.get_object()
        try:
            if(userToFollow == request.user.bethovenUser):
                (success,message) = (0, "Impossible to follow yourself")
            elif request.user.bethovenUser.following.filter(pk=pk).exists():
                (success,message) = (0, f"Already following {userToFollow.user.username}")
            else:
                request.user.bethovenUser.following.add(userToFollow)
                (success,message) = (1, f"You are now following {userToFollow.user.username}")
        except Exception:
            (success,message) = (0, "Follow failed")
        finally:  
            return Response({   
                        "success" : success,
                        "message" : message
            })
    
    @action(detail=True)
    def unfollow(self, request, pk):
        """Make a user unfollower another user - takes care that :
            * The user is not itself
            * The user is currently followed by the requesting user
        """
        userToUnfollow = self.get_object()
        try:
            if(userToUnfollow == request.user.bethovenUser):
                (success,message) = (0, "Impossible to unfollow yourself")
            elif not request.user.bethovenUser.following.filter(pk=pk).exists():
                (success,message) = (0, f"Can not unfollow {userToUnfollow.user.username} as you do not follow him")
            else:
                request.user.bethovenUser.following.remove(userToUnfollow)
                (success,message) = (1, f"You have unfollowed {userToUnfollow.user.username}")
        except Exception:
            (success,message) = (0, "Unfollow failed")
        finally:
            return Response({   
                        "success" : success,
                        "message" : message
            })

    @action(detail=False)
    def search(self, request):
        """Search a user according to its username"""
        # fetch request parameters : Username for search, coins for order if necessary
        username = request.GET.get("username", "")
        ordering = request.GET.get("coins")
        #analyse "ordering" value - default at "updated_at", can be coins. asc or desc determine the order of sorting
        if not ordering:
            ordering = "updated_at" #default
        else:
            if ordering not in ["asc", "desc"] : 
                #only asc,desc permitted (ex: coincs=asc)
                return Response({"message": "'coins' parameters only take asc or desc values"}, status=status.HTTP_400_BAD_REQUEST)
            ordering = f"-coins" if ordering=="desc" else "coins"
        #Make the request, using a regex to find all user with the parameter as a part of their username
        users = BethovenUser.objects.filter(user__username__regex=fr"(?i).*{username}.*").order_by(ordering)
        serializer = BethovenProfileCard(users, many=True) #build a list of profile cards
        return Response(serializer.data)

class BetViewSet(ViewsetFunctionPermissions):
    """ Bet Viewset (controller) """
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

    permission_classes = [AllowAny]
    permission_classes_by_action = {
                                    'create': [IsAuthenticated], #Must be registered to create a bet
                                    'partial_update': [isBetOwner], #allow th bet owner to close or reveal
                                    'destroy' : [isBetOwner], #allow th bet owner to delete the bet,
                                    'gamble' : [IsAuthenticated]
                                }

    def create(self,request):
        serializer = CreateBetSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            bet = serializer.save()
            bet.owner = request.user.bethovenUser
            bet.save()
            return Response({
                "Bet" : BetSerializer(bet).data,
                "message": "Bet Created Successfully."
            })

    def perform_destroy(self,instance):
        if not instance.result : 
            instance.refund()
        instance.delete()

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self,request,pk):

        serializer = PartialUpdateBetSerializer(self.get_object(), data = request.data)

        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response({"message": "Bet updated succesfully",})  


    def get_permissions(self):
        """Function that allow for defining permissions by function"""
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    @action( detail = True, methods=['post'])
    def gamble(self,request,pk):
        serializer = GambleUserBetSerializer(data = request.data)

        user = request.user.bethovenUser
        bet = Bet.objects.get(pk=pk)

        if serializer.is_valid(raise_exception = True):
            if(bet.isClosed):
                return Response({"message" : 'This bet is closed !'})

            if UserBet.objects.filter(user=user,bet=bet):
                return Response({"message" : 'You have already bet !'})
            

            amount = request.data['amount']
            choice = request.data['choice']

            if user.coins < amount :
                return Response({"message" : 'You are ruined !'})


            userBet = UserBet(amount=amount,choice=choice,user=user,bet=bet)
            userBet.save()
            user.coins -= amount
            user.save()
            bet.save()
            return Response({
                "Your bet" : UserBetSerializer(userBet).data,
                "message": "Bet Successfully."
            })
           
