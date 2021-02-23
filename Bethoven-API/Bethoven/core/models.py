from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BethovenUser(models.Model):
    """This model extends the User basic authentication model, while the economy field"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField