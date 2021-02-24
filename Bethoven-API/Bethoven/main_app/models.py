from django.db import models
from django.contrib.auth.models import User

#Timestamped abstract model
class TimeStampedModel(models.Model):
    """Abstract model that add the timestamps created_at and updated_at"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BethovenUser(TimeStampedModel):
    """Model linked to the User basic authentication model, while the economy field

    Parameters: coins, user for user standard params
    Has timestamp : created_at, updated_at
    
    Relationships :
    Usage : 'following = user.following.all()' 
        * user.following to have the users this user follows
        * user.followers to have the user currently following this one
        * user.BetsOwned to have the bets created by the user
        * user.UserBets to have the bets this user has bet on
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField()

    # many-to-many in itself, needs to be asymetrical
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

class Bet(TimeStampedModel):
    """Model that represent a bet with its description, choices, and closure mecanism

    Parameters : title, description, choice1, choice2, isClosed, result
    Has timestamp : created_at, updated_at
    
    Relationships :
        * bet.owner to see the owner of this bet (nullable)
        * bet.usersBetting to see the users currently betting on this bet
        """
    #Bet gestion
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=50)    
    choice2 = models.CharField(max_length=50)
    #Closure gestion
    isClosed = models.BooleanField(default=False)
    result = models.IntegerField(blank=True, null=True)
    #"Own" relationship with user. Nullable as we dont want the bets to be destroyed on user deletion
    owner = models.ForeignKey(BethovenUser, related_name='BetsOwned', on_delete=models.SET_NULL, null=True)

    #When a user does a bet
    usersBetting = models.ManyToManyField(BethovenUser, through='UserBet', related_name='BetsDone')

class UserBet(TimeStampedModel):
    """Relatioship table when a user bet on a bet. Bet bet bet bet bet. Bet is the wrose word in tne english language >:-(
        
    Parameters: choice, amount
    Has timestamp : created_at, updated_at
    
    Relationship to :
        * UserBet.user : the user that bet on the bet
        * UserBet.bet : The bet
        """
    #Source : https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships 'adding fields to many-to-many relationships'
    user = models.ForeignKey(BethovenUser, on_delete=models.CASCADE)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    choice = models.IntegerField()
    amount = models.IntegerField()

class Comment(TimeStampedModel):
    """Model that represent a comment from a user on a bet
    
    Parameters : text
    Has timestamp : created_at, updated_at
    
    Relationship to :
        * Comment.user - the user that created this comment
        * Comment.bet - the bet on which this comment is located
    """
    text = models.CharField(max_length=200)
    user = models.ForeignKey(BethovenUser, on_delete=models.CASCADE)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)