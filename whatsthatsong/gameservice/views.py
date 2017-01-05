from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import JSONParser

from gameservice.models import Game, Track, GuessQueue
from gameservice.serializers import GameSerializer, TrackSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by('-started_datetime')
    serializer_class = GameSerializer

    @list_route(methods=['post'])
    def buzz_in(self, request):
        """
        This method is called by the controller when a button is pressed and
        queues the player to await a guess to be made.
        """
        queue_size = len(GuessQueue.objects.all())
        if queue_size == 0:
            data = JSONParser().parse(request)
            print 'Queuing player %d' % data.get('player_id')
            new_queue = GuessQueue()
            new_queue.player = data.get('player_id')
            new_queue.save()

        return Response({'status': 'ok'})

    @list_route(methods=['post'])
    def make_guess(self, request):
        """
        Following a player "buzzing in" this should be called to supply that
        players guess having been speech recognised. This adds the guess to the
        queued player.
        """
        data = JSONParser().parse(request)
        queue = GuessQueue.objects.all()[0]
        queue.guess = data.get('guess')
        queue.save()
        print 'Guess: %s' % data.get('guess')
        return Response({'status': 'ok'})

    @detail_route()
    def state(self, request, pk=None):
        """
        Return the state of the game with the id supplied by "pk". State returns
        whether a buzzer has been pressed via a non-zero number in
        'guess_player_id'. What the current guess is and whether or not the
        guess was correct in the 'guess_state' property.
        """
        game = get_object_or_404(Game, pk=pk)

        response_data = {
            'guess_player_id': 0,
            'guess': '',
            'guess_status': 'WRONG',
        }

        # There will only ever be one guess in the queue so here we're just
        # essentially testing if its empty or not. If the queue is empty we
        # dont need to do anything and just return the default game state.
        all_guesses = GuessQueue.objects.all()
        if len(all_guesses) == 1:
            # We found a player in the queue so set up the appropriate response.
            guess = all_guesses[0]
            response_data['guess_player_id'] = guess.player
            response_data['guess'] = guess.guess

            if guess.guess != "" and guess.guess is not None:
                # Lower case and remove punctuation as per the rules defined in
                # the normalize_match_term method.
                search_guess = ',%s,' % Track.normalize_match_term(guess.guess)
                match_terms = game.track.match_terms

                # Try and find the guess in the possible match terms, if its
                # found then the guess was correct.
                print match_terms
                print search_guess

                if match_terms.find(search_guess) >= 0:
                    response_data['guess_status'] = 'CORRECT'

                # This guess has now been processed so remove it from the queue.
                guess.delete()

        return Response(response_data)

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

def game_ui(request):
    """
    Return the single page web app that is the game UI.
    """
    return render_to_response(
        'whatsthatsong.html',
        context_instance=RequestContext(request)
        )
