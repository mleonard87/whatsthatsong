import RPi.GPIO as GPIO
import time


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
        print('Player One')
    if input_state2 == False:
        print('Player Two')
    if input_state3 == False:
        print('Player Three')
    if input_state4 == False:
        print('Player Four')

    time.sleep(0.2)
