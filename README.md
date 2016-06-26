# Whats That Song?

A project built for a Raspberry Pi that allows a game to be played for 1-4 players where a song is played and players buzz-in to shout out their guess.

# Structure

The project is broken into two main parts.

The [whatsthatsong](https://github.com/mleonard87/whatsthatsong/tree/master/whatsthatsong) directory contains a django app which exposes a RESTful API to power the game and integrate with the controller as well power the single page web app. The single page web app is also driven via the Django app and served as a regular Django template.

In the  [controller](https://github.com/mleonard87/whatsthatsong/tree/master/controller) directory there is a python script called [buzzer_and_listen.py](https://github.com/mleonard87/whatsthatsong/blob/master/controller/buzzer_and_listen.py) which runs an event loop to detect the button presses via the Raspberry Pis GPIO pins and then issue an HTTP request to a REST API provided by the Django app.

# Note

No songs have been included as part of this respoitory due to licensing restrictions. To add songs, place them in /whatsthatsong/gameservice/static/media and add entries to the Track model. The filename field on the Track object should be the filename without an extension.

Tracks must be in `.mp3` format and should also have a 300x300px album art file in the same directory. This should be n Jpeg format with a `.jpg` extension.

The match_terms field should be a CSV list of terms you wish to match on when the player shouts out their guess. You do not need to include the artist or track title in this.
