from channels import Group
from channels.sessions import channel_session

from .models import Game, Track

import json

@channel_session
def ws_connect(message):
    suffix = message['path'].strip('/').split('/')[1]
    print 'registered:'
    print suffix
    if suffix == 'game':
        Group('game').add(message.reply_channel)

    if suffix == 'controller':
        Group('controller').add(message.reply_channel)


@channel_session
def ws_receive(message):
    print 'RECEIVE'
    print message
    data = json.loads(message['text'])

    print data['action']
    print data

    if data['action'] == 'GAME_NEW':
        g = Game()
        g.track = Track.random()
        print '---'
        print g.track.title
        print g.track.match_terms
        print '---'
        g.save()
        m = {
            'action': 'GAME_CREATED',
            'gameId': g.id,
            'trackId': g.track.id,
            'filename': g.track.filename,
            'title': g.track.title,
            'artist': g.track.artist,
        }
        print m
        Group('game').send({'text': json.dumps(m)})
        return

    if data['action'] == 'PLAYER_JOIN':
        m = {
            'action': 'PLAYER_JOIN',
            'player': data['player'],
        }
        Group('game').send({'text': json.dumps(m)})
        return

    if data['action'] == 'PLAYER_LEAVE':
        m = {
            'action': 'PLAYER_LEAVE',
            'player': data['player'],
        }
        Group('game').send({'text': json.dumps(m)})
        return

    if data['action'] == 'PLAYER_BUZZ_IN':
        m = {
            'action': 'PLAYER_BUZZ_IN',
            'player': data['player'],
        }
        Group('game').send({'text': json.dumps(m)})
        return

    if data['action'] == 'PLAYER_GUESS':
        guess = data['guess']
        g = Game.objects.get(id=data['gameId'])
        search_guess = ',%s,' % Track.normalize_match_term(guess)
        match_terms = g.track.match_terms

        status = 'WRONG'
        print '***'
        print match_terms
        print search_guess
        print '***'
        if match_terms.find(search_guess) >= 0:
            status = 'CORRECT'

        m = {
            'action': 'PLAYER_GUESS',
            'player': data['player'],
            'guess': data['guess'],
            'status': status
        }
        Group('game').send({'text': json.dumps(m)})
        return

    if data['action'] == 'GAME_START':
        m = {
            'action': 'GAME_START',
            'gameId': data['gameId'],
        }
        Group('controller').send({'text': json.dumps(m)})
        return

    if data['action'] == 'GAME_LOAD':
        m = {
            'action': 'GAME_LOAD',
        }
        Group('controller').send({'text': json.dumps(m)})
        return

    if data['action'] == 'GAME_END':
        m = {
            'action': 'GAME_END',
        }
        Group('controller').send({'text': json.dumps(m)})
        return

    if data['action'] == 'GAME_ANNOUNCE_ID':
        m = {
            'action': 'GAME_ANNOUNCE_ID',
            'gameId': data['gameId'],
        }
        Group('controller').send({'text': json.dumps(m)})
        return

    if data['action'] == 'GAME_RESUME':
        m = {
            'action': 'GAME_RESUME',
            'gameId': data['gameId'],
        }
        Group('controller').send({'text': json.dumps(m)})
        return

@channel_session
def ws_disconnect(message):
    print 'DISCONNECT'
    print message
    # label = message.channel_session['room']
    # Group('chat-'+label).discard(message.reply_channel)
