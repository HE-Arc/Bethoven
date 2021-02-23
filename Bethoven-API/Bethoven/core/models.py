from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BethovenUser(models.Model):
    """Model linked to the User basic authentication model, while the economy field"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField()

    # many-to-many in itself, needs to be asymetrical
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    #Gives access to
        #following = user.following.all()
        #followers = user.followers.all()

class Bet(models.Model):
    """Model that represent a bet with its description, choices, and closure mecanism"""
    #Bet gestion
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=50)    
    choice2 = models.CharField(max_length=50)
    #Closure gestion
    isClosed = models.BooleanField(default=False)
    result = models.IntegerField(blank=True, null=True)
    #"Own" relationship with user. Nullable as we dont want the bets to be destroyed on user deletion
    owner = models.ForeignKey(BethovenUser, related_name='Bets', on_delete=models.SET_NULL, null=True)