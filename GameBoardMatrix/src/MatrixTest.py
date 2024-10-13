import RPi.GPIO as GPIO
import time

def matrixInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Set up GPIO inputs 3, 5, 7, 8
    GPIO.setup(3, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(5, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(7, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(8, GPIO.IN, GPIO.PUD_UP)
    #GPIO.setup(8,GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(10, GPIO.IN, GPIO.PUD_UP)
