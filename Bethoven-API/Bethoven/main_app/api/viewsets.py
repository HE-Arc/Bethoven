
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .custom_perm import isSelfUser , isBetOwner
from .custom_exceptions import UserUpdateError
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
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
                "success": "User Created Successfully !",
            })

    def destroy(self, request, *args, **kwargs):
        """
        The Destroy function should not only destroy the bethoven user, but also the linked Auth.User.
        As the delete is on cascade, deleting the user is enough to delete the bethoven user.
        """
        bethovenUser = self.get_object()
        bethovenUser.user.delete()
        return Response({
                "success": "User deleted succesfully",
            })

    def update(self, request, *args, **kwargs):
        """The update method uses the updateserilalizer that verifies the password is the good one before applying any change"""
        serializer = BethovenUpdateSerializer(self.get_object(), data=request.data)
        try:
            if serializer.is_valid():
                serializer.save(user=request.user.username)
                return Response({"success":1, "message": "User updated succesfully",})
        except UserUpdateError as e :
            return Response({"error": str(e)}, status = HTTP_422_UNPROCESSABLE_ENTITY)


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
        lastBetsSerializer = BetSerializer(user.last_bets(5), context={'request': request}, many=True)                #a standardized list of profiles and bets
        return Response({
            "user" : userProfileSerializer.data,
            "follows" : followersProfilesSerializers.data,
            "statistics" : user.get_statistics(),
            "lastBets" : lastBetsSerializer.data,
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

    @action(detail=True, methods=['post'])
    def addcoins(self, request, pk):
        try:
            user = self.get_object()
            user.coins += 15
            user.save()
            return Response({"success" : "Added 15betcoins to your account"})
        except :
            return Response({"error" : "Couldn't add coins to your account"})

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
                (level,message) = ("warning", "Impossible to follow yourself")
            elif request.user.bethovenUser.following.filter(pk=pk).exists():
                (level,message) = ("info", f"Already following {userToFollow.user.username}")
            else:
                request.user.bethovenUser.following.add(userToFollow)
                (level,message) = ("success", f"You are now following {userToFollow.user.username}")
        except Exception:
            (level,message) = ("error", "Follow failed")
        finally:  
            return Response({   
                        level : message,
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
                (level,message) = ("warning", "Impossible to unfollow yourself")
            elif not request.user.bethovenUser.following.filter(pk=pk).exists():
                (level,message) = ("info", f"Can not unfollow {userToUnfollow.user.username} as you do not follow him")
            else:
                request.user.bethovenUser.following.remove(userToUnfollow)
                (level,message) = ("success", f"You have unfollowed {userToUnfollow.user.username}")
        except Exception:
            (level,message) = ("error", "Unfollow failed")
        finally:
            return Response({   
                        level : message,
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
        if not username :
                return Response({"message": "You must provide a username to search"}, status=status.HTTP_400_BAD_REQUEST)
        #Make the request, using a regex to find all user with the parameter as a part of their username
        users = BethovenUser.objects.filter(user__username__icontains=username).order_by(ordering)
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
                                    'gamble' : [IsAuthenticated], #Must be authenticated to gamble (coins from account)
                                    'home' : [IsAuthenticated], #Must be authenticated to retrieve friend bets.
                                    'mybet' : [IsAuthenticated], #bet by user - must be authenticated,
                                }

    def create(self,request):
        serializer = CreateBetSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            bet = serializer.save()
            bet.owner = request.user.bethovenUser
            bet.save()
            return Response({
                "bet" : BetSerializer(bet, context={'request': request}).data,
                "success": "Bet Created Successfully."
            })

    def perform_destroy(self,instance):
        if  instance.result is not None : 
            instance.refund()
        instance.delete()

    def update(self, request, pk=None):
        response = {'error': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


    ### FEEDS From bet ###
    def list(self, request):
        """ List gives a trending feed as it requires no auth and is the 'landing page' of bethoven """
        serializer = FeedSerializer(data = request.query_params)
        if serializer.is_valid(raise_exception = True):
            #only 2 choices : trending of hot
            ordering = serializer.data["order"]
            trending = True if ordering == "trending" else False
            bets = Bet.trending_bets_from_id(serializer.data["number"], serializer.data["betFrom"], trending)
            return Response(BetSerializer(bets, context={'request': request}, many=True).data)

    @action(detail = False)
    def home(self, request):
        """ List gives a trending feed as it requires no auth and is the 'landing page' of bethoven """
        serializer = FeedSerializer(data = request.query_params)
        if serializer.is_valid(raise_exception = True):
            bets = Bet.friend_bets(serializer.data["number"], serializer.data["betFrom"], request.user.bethovenUser)
            return Response(BetSerializer(bets, context={'request': request}, many=True).data)

    @action(detail = False)
    def mybet(self, request):
        """ List gives a trending feed as it requires no auth and is the 'landing page' of bethoven """
        serializer = FeedSerializer(data = request.query_params)
        if serializer.is_valid(raise_exception = True):
            bets = Bet.betByUser(serializer.data["number"], serializer.data["betFrom"], request.user.bethovenUser)
            return Response(BetSerializer(bets, context={'request': request}, many=True).data)

    def partial_update(self,request,pk):
        """ Close/reveal done through patch in the serializer 'update' method"""
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
                return Response({"error" : 'This bet is closed !'})

            if UserBet.objects.filter(user=user,bet=bet):
                return Response({"info" : 'You have already bet !'})

            amount = request.data['amount']
            choice = request.data['choice']

            if amount <= 0 :
                return Response({"warning" : 'You have to bet at least 1 betcoin !'})

            if user.coins < amount :
                return Response({"error" : 'You are ruined !'})


            userBet = UserBet(amount=amount,choice=choice,user=user,bet=bet)
            userBet.save()
            user.coins -= amount
            user.save()
            bet.save()
            return Response({
                "Your bet" : UserBetSerializer(userBet).data,
                "success": "Bet Successfully."
            })
