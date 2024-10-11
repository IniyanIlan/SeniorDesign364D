import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(10, GPIO.IN, GPIO.PUD_UP)

while True:
    if not GPIO.input(10):
        GPIO.output(8, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(8, GPIO.LOW)
        time.sleep(1)