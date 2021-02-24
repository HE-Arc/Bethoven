from django.contrib import admin
from main_app.models import Bet, BethovenUser, UserBet, Comment

# Register your models here.

admin.site.register(BethovenUser)
admin.site.register(Bet)
admin.site.register(UserBet)
admin.site.register(Comment)