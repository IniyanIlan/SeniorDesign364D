import RPi.GPIO as GPIO
import time

# Simple program made to test GPIO pin usage on the RPI 5.
# Pressing the button 4 times will end the program.

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN)
n = 0
flag = True
while flag:
    if GPIO.input(10):
        GPIO.output(8, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(8, GPIO.LOW)
        time.sleep(1)
        n += 1
        if(n > 3):
            flag = False
        