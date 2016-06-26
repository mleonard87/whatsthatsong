import RPi.GPIO as GPIO
import speech_recognition as sr

import json
import time
import urllib2
import sys

if len(sys.argv) == 1:
    print "Error:"
    print "  You must supply a game service server."
    print "  Usage: python buzzer_and_listen.py <host_name_or_ip_and_port>"
    sys.exit(1)

GAME_SERVICE_SERVER = sys.argv[1]

def request_buzz_in(player_id):
    print 'BUZZ %d' % player_id
    body = {
        'player_id': player_id
    }

    req = urllib2.Request('http://%s/api/games/buzz_in/' % GAME_SERVICE_SERVER)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(body))

def request_guess(guess):
    print 'Guess %s' % guess
    body = {
        'guess': guess
    }

    req = urllib2.Request('http://%s/api/games/make_guess/' % GAME_SERVICE_SERVER)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(body))

def capture_guess(player_id):
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
    request_buzz_in(button_id)
    guess = capture_guess(button_id)
    request_guess(guess)

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
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

    time.sleep(0.2)
