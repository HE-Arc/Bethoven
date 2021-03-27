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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bethovenUser")
    coins = models.IntegerField()
    
    # many-to-many in itself, needs to be asymetrical
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    @classmethod
    def create_bethoven_user(cls, username, email, password):
        bethovenUser = cls()
        bethovenUser.user = User.objects.create_user(username=username, email=email,password=password)
        bethovenUser.coins = 30
        bethovenUser.save()
        return bethovenUser

    def get_statistics(self):
        """ Return the bet statistics of this user """
        #init variables
        userBets = UserBet.objects.filter(user=self)
        totalBet = len(userBets)
        results = {0:0, 1:0}
        totalBetAmount = 0
        totalWinAmount = 0
        #loop through userbets of the user (fetch once, avoid N+1) to find its bet statistics
        for userBet in userBets:
            totalBetAmount += userBet.amount
            if userBet.bet.result is not None :
                results[1 if userBet.bet.result == userBet.choice else 0]+=1
                if userBet.gain is not None :
                    totalWinAmount += userBet.gain

        won = results[1]
        lost = results[0]
        effectiveness = 1.0 if lost == 0 else (won-lost)/(won+lost)

        return {
            "Won": won,
            "Lost": lost,
            "total bet ": totalBet,
            "totalBetAmount": totalBetAmount,
            "totalWinAmount": totalWinAmount,
            "Effectiveness": effectiveness,
        }

    def last_bets(self, number):
        """ Return the last 5bets of this user """
        return [userbets.bet for userbets in UserBet.objects.filter(user=self).order_by("created_at")[:number]]

    def __str__(self):
        return self.user.username
    
    def __hash__(self):
        return self.id

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
    choice0 = models.CharField(max_length=50)
    choice1 = models.CharField(max_length=50)
    #Closure gestion
    isClosed = models.BooleanField(default=False)
    result = models.IntegerField(default=None, blank=True, null=True)
    #"Own" relationship with user. Nullable as we dont want the bets to be destroyed on user deletion
    owner = models.ForeignKey(BethovenUser, related_name='BetsOwned', on_delete=models.SET_NULL, null=True)

    #When a user does a bet
    usersBetting = models.ManyToManyField(BethovenUser, through='UserBet', related_name='BetsDone')

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return isinstance(self, Bet) and isinstance(other, Bet) and self.id == other.id 

    def __hash__(self):
        return self.id

    def __lt__(self, other):
        return self.id < other.id
    
    def refund(self): 
        """Refund every user that has bet on this bet of their gambled amount"""
        userBets = UserBet.objects.filter(bet=self)
        for userBet in userBets:
            userBet.user.coins += userBet.amount
            userBet.user.save()

    def bet_ratio(self):
        """Return the ratio choice0 / choice1 of this bet"""
        choiceCount = { 0 : 0, 1 : 0 }
        total = number = 0
        for userBet in UserBet.objects.filter(bet=self):
            number += 1
            total += userBet.amount
            try:
                choiceCount[userBet.choice] += userBet.amount
            except KeyError :
                choiceCount[userBet.choice] = userBet.amount
        return {
            "number" : number,
            "total" : total,
            "ratio" : {k : self.get_ratio(v, total) for k,v in choiceCount.items()}
        }

    def get_ratio(self, value, total) :
        if total == 0 : return 0 #avoid /0
        return int(100*round(value/total,2))

    @classmethod
    def trending_bets_from_id(cls, number, id, trending=True):
        """ Return the last $number bets starting from the $id, either hot (last created) or trending (last updated)"""
        orderBy = "-updated_at" if trending else "-created_at"
        bets = Bet.objects.filter(isClosed=False).order_by(orderBy)
        
        if id is not None :
            limitBet = Bet.objects.get(id=id)
            if trending :
                bets = bets.filter(updated_at__lt=limitBet.updated_at)
            else :
                bets = bets.filter(created_at__lt=limitBet.created_at)

        return bets[:number]

    @classmethod
    def friend_bets(cls, number, id, user):
        """ Return the "home" feed of a user : the bets from his friends"""
        follows = user.following.all()

        betsFriendsOwn = Bet.objects.filter(owner__in=follows).order_by('-updated_at')
        betsFriendsParticipate = UserBet.objects.filter(user__in=follows).order_by('-updated_at')

        if id is not None :
            limitBet = Bet.objects.get(id=id)
            betsFriendsOwn = betsFriendsOwn.filter(updated_at__lt=limitBet.updated_at)
            betsFriendsParticipate = betsFriendsParticipate.filter(bet__updated_at__lt=limitBet.updated_at)

        betsFriendsOwn = list(betsFriendsOwn)
        betsFriendsParticipate = [userbet.bet for userbet in betsFriendsParticipate]
        allBetsUnique = list(set(betsFriendsOwn + betsFriendsParticipate))
        allBets = sorted(allBetsUnique, key=lambda x : x.updated_at, reverse=True)
        return allBets[:number]
      
    @classmethod
    def betByUser(cls, number, id, user):
        """ Return the "mybet" feed, which can have the bets which the user owns or participate in """
        betsOwned = Bet.objects.filter(owner=user).order_by('-id')
        betsParticipating = UserBet.objects.filter(user=user).order_by('-id')

        if id is not None :
            betsOwned = betsOwned.filter(id__lt=id)
            betsParticipating = betsParticipating.filter(bet__lt=id)
            
        betsOwned = list(betsOwned)
        betsParticipating = [userbet.bet for userbet in betsParticipating]
        allBetsUnique = list(set(betsOwned + betsParticipating))
        allBets = sorted(allBetsUnique, key=lambda x : x.id, reverse=True)
        return allBets[:number]

    def give(self):
        """Give to winners the amount """
        #init
        userBets = UserBet.objects.filter(bet=self)
        winners = []
        totalBetAmount = 0
        totalBetWinner = 0

        #go through userbets for this bet
        for userBet in userBets:
            #keep track of the amount
            totalBetAmount += userBet.amount
            #winners go into the winner pool
            if userBet.choice == userBet.bet.result:
                totalBetWinner += userBet.amount
                winners.append(userBet)
            else :
                #loosers have 0
                userBet.gain = 0
                userBet.save()

        #go through winners to give them their gain (need totalamount and winner amount)
        for userBet in winners:
            gain = (userBet.amount / totalBetWinner) * totalBetAmount
            #give gain to user
            userBet.user.coins += int(round(gain))
            userBet.user.save()
            #save gain into userbet
            userBet.gain = gain
            userBet.save()

class UserBet(TimeStampedModel):
    """
    Relatioship table when a user bet on a bet. Bet bet bet bet bet. Bet is the wrose word in tne english language >:-(
        
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
    gain = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.user} bet:{self.amount} on {self.choice}'

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