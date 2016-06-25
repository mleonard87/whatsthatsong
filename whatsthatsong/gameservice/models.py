from __future__ import unicode_literals

from django.db import models
from django.db.models import Count

import random

class Track(models.Model):
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    filename = models.CharField(max_length=510)

    @staticmethod
    def random():
        count = Track.objects.all().aggregate(count=Count('id'))['count']
        random_id = random.randint(1, count)
        return Track.objects.get(pk=random_id)

class Game(models.Model):
    PLAYER_CHOICES = (
        ('PLAYER_ONE',   u'Player One'),
        ('PLAYER_TWO',   u'Player Two'),
        ('PLAYER_THREE', u'Player Three'),
        ('PLAYER_FOUR',  u'Player Four'),
        )

    started_datetime = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey(Track, blank=True)
    winner = models.CharField(max_length=20, choices=PLAYER_CHOICES, null=True, blank=True)

class GuessQueue(models.Model):
    player = models.IntegerField()
    guess = models.CharField(max_length=1000, null=True, blank=True)
