import RPi.GPIO as GPIO
import time


def main():
    matrixInit()
    #Initialize 2d array
    rows, cols = (2,2)
    gameBoard = [[0] * cols] * rows
    while(not GPIO.input(10)):
        n += 1
        n -= 1 # do nothing




def matrixInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Set up GPIO inputs 3, 5, 7, 8
    GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN) # pos 1 
    GPIO.setup(5, GPIO.IN, GPIO.PUD_DOWN) # pos 2
    GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN) # pos 3
    GPIO.setup(8, GPIO.IN, GPIO.PUD_DOWN) # pos 4
    # Set edge detection functions
    GPIO.add_event_detect(3, GPIO.RISING, setTopLeft, 20)
    GPIO.add_event_detect(5, GPIO.RISING, setTopRight, 20)
    GPIO.add_event_detect(7, GPIO.RISING, setBotLeft, 20)
    GPIO.add_event_detect(8, GPIO.RISING, setBotRight, 20)
    #GPIO.setup(8,GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN)

def setTopLeft():
    print("Player moved to space 1!")

def setTopRight():
    print("Player moved to space 2!")

def setBotLeft():
    print("Player moved to space 3")

def setBotRight():
    print("Player moved to space 4!")


if __name__ == "__main__":
    main()