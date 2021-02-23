from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BethovenUser(models.Model):
    """Model linked to the User basic authentication model, while the economy field"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField
    
    # many-to-many in itself, needs to be asymetrical
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    #Gives access to
        #following = user.following.all()
        #followers = user.followers.all()