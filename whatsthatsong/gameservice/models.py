from __future__ import unicode_literals

from django.db import models
from django.db.models import Count

import random, string

class Track(models.Model):
    """
    Model object representation a track that is available to guess. For example,
    'Hotel California' by 'The Eagles'.
    """
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    filename = models.CharField(max_length=510)
    match_terms = models.CharField(max_length=1000)

    @staticmethod
    def random():
        """
        Return a random track from the database.
        """
        count = Track.objects.all().aggregate(count=Count('id'))['count']
        random_id = random.randint(1, count)
        return Track.objects.get(pk=random_id)

    @staticmethod
    def normalize_match_term(raw_match_term):
        """
        Take a search/match term for a track, lower case it and remove the
        punctuation.

        :param raw_match_term: An unaltered match term to be cleaned.
        """
        for ch in '-\'!.':
            match_term = raw_match_term.replace(ch, '')

        match_term = match_term.lower()

        return match_term

    def save(self, *args, **kwargs):
        """
        Overidden the default save method to ensure that the match_terms is
        fully lower case, has the expected preceeding and trailing commas for
        in-string matching and has all punctuation removed.
        """
        if not self.match_terms.startswith(','):
            self.match_terms = ',%s' % self.match_terms

        if not self.match_terms.endswith(','):
            self.match_terms = '%s,' % self.match_terms

        if self.match_terms.find(self.artist.lower()) < 0:
            self.match_terms = '%s%s,' % (self.match_terms, self.artist.lower())

        if self.match_terms.find(self.title.lower()) < 0:
            self.match_terms = '%s%s,' % (self.match_terms, self.title.lower())

        self.match_terms = Track.normalize_match_term(self.match_terms)

        super(Track, self).save(*args, **kwargs)


class Game(models.Model):
    """
    A model object representing an instance of a game being played.
    """
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
    """
    This acts a queue (although realistically it only ever has one item in it at
    a time). This tracks when a buzzer has been pressed and what artist/track
    title has been guessed.
    """
    player = models.IntegerField()
    guess = models.CharField(max_length=1000, null=True, blank=True)
