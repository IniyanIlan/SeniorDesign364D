import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN)

while(not GPIO.input(10)):
    print("Hall effect reads: ", GPIO.input(8))
    time.sleep(1)