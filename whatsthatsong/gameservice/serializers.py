from gameservice.models import Game, Track, GuessQueue
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('pk', 'started_datetime', 'track', 'winner')

    def create(self, request):
        """
        Overidden create method to able to the assignment of a random track.
        """
        queue_size = len(GuessQueue.objects.all())
        if queue_size != 0:
            GuessQueue.objects.all()[0].delete()

        game = Game()
        game.track = Track.random()
        game.save()

        return game

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('pk', 'artist', 'title', 'filename')
