from django.db import models
from django.contrib.auth.models import User
from api.createField import createMineField
from django.contrib.postgres.fields import JSONField

class Game(models.Model):

    player1 = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='player1')
    player2 = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='player2')
    player1score =  models.IntegerField(default=0, blank=True)
    player2score =  models.IntegerField(default=0, blank=True)
    turn = models.BooleanField(default=True)
    name = models.CharField(max_length=100, blank=True, default='')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    winner = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='winner')
    mineFieldSetup = JSONField(blank=True, default=createMineField(15, 15, 51))



    def __str__(self):
        if(self.winner):
            return ('Game ' + self.name + ' ' + 'is won by: ' + self.winner.username)
        elif (self.player1 and self.player2):
            return ('Game: ' + self.name + ' STILL PLAYING BY: ' + self.player1.username + ' vs ' + self.player2.username + ' CREATED ON DATE: ' + str(self.date))
        elif (self.player1):
            return ('Game: ' + self.name + ' STILL PLAYING BY: ' + self.player1.username + ' vs ' + ' CREATED ON DATE: ' + str(self.date))
        elif (self.player2):
            return ('Game: ' + self.name + ' STILL PLAYING BY: ' + self.player2.username + ' vs ' + ' CREATED ON DATE: ' + str(self.date))
        else:
            return ('Game: ' + self.name + ' STILL PLAYING BY: ' + 'CREATED ON DATE: ' + str(self.date))

@property
def score(self):
    return self.winner.count()

User.add_to_class('score', score)
