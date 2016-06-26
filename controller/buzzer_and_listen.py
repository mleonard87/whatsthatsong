import RPi.GPIO as GPIO
import speech_recognition as sr

import json, time, urllib2, sys

# Initial sanity checking of lanching this script.
if len(sys.argv) == 1:
    print "Error:"
    print "  You must supply a game service server."
    print "  Usage: python buzzer_and_listen.py <host_name_or_ip_and_port>"
    sys.exit(1)

GAME_SERVICE_SERVER = sys.argv[1]

def request_buzz_in(player_id):
    """
    Handle making the request to the game service API when a buzzer
    is pressed.

    :param played_id: The id of the player/buzzer (1-4).
    """
    print 'BUZZ %d' % player_id
    body = {
        'player_id': player_id
    }

    req = urllib2.Request('http://%s/api/games/buzz_in/' % GAME_SERVICE_SERVER)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(body))

def request_guess(guess):
    """
    Handle making the request to the game service API when a guess have been
    made and speech recognised to text.

    :param guess: The guess made as convert from speech to text.
    """
    print 'Guess %s' % guess
    body = {
        'guess': guess
    }

    req = urllib2.Request('http://%s/api/games/make_guess/' % GAME_SERVICE_SERVER)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(body))

def capture_guess(player_id):
    """
    Once a buzzer has been pressed start listening on the microphone and use the
    Google Speech Recognition service via the Python speech_recongition library
    to conver the audio input to text.

    :param player_id: The id of the player/buzzer (1-4).
    :return: Return the text representation of the audio input.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return "[UNKNOWN]"

def process_button_press(button_id):
    """
    Handle when a buzzer is pressed by logging the button press with the game
    service, then capture the audio and lodge the guess.

    :param button_id: The id of the player/buzzer (1-4).
    """
    request_buzz_in(button_id)
    guess = capture_guess(button_id)
    request_guess(guess)

GPIO.setmode(GPIO.BCM)

# Set up the GPIO pins we're going to use.
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    """
    Infinite loop waiting on input from the various GPIO pins that are being
    listened on. If an input is detected called 'process_button_press'.
    """
    input_state1 = GPIO.input(18)
    input_state2 = GPIO.input(23)
    input_state3 = GPIO.input(24)
    input_state4 = GPIO.input(25)

    if input_state1 == False:
        process_button_press(1)
    if input_state2 == False:
        process_button_press(2)
    if input_state3 == False:
        process_button_press(3)
    if input_state4 == False:
        process_button_press(4)

    # Sleep for a fraction of a second here to deal with the button being
    # pressed slightly longer than expected and being registered as multiple
    # button presses.
    time.sleep(0.2)
