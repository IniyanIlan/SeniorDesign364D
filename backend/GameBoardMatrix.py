import RPi.GPIO as GPIO
import time
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np


# Access the shared memory by name
shm_name = 'Matrix'  # Replace with actual shm.name from main process
array_shape = (5, 8)  # Same shape as created initially
array_dtype = np.int8  # Same dtype as initially created

# Connect to the existing shared memory block
existing_shmMatrix = shared_memory.SharedMemory(name=shm_name)

# Create a 2D NumPy array using the existing shared memory
shared_array = np.ndarray(array_shape, dtype=array_dtype, buffer=existing_shmMatrix.buf)


def matrixInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Set up GPIO inputs 3, 5, 7, 8
    GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN) # pos 1 
    GPIO.setup(5, GPIO.IN, GPIO.PUD_DOWN) # pos 2
    GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN) # pos 3
    GPIO.setup(8, GPIO.IN, GPIO.PUD_DOWN) # pos 4
    # Set edge detection functions
    GPIO.add_event_detect(3, GPIO.FALLING, setTopLeft, 20)
    GPIO.add_event_detect(5, GPIO.FALLING, setTopRight, 20)
    GPIO.add_event_detect(7, GPIO.FALLING, setBotLeft, 20)
    GPIO.add_event_detect(8, GPIO.FALLING, setBotRight, 20)
    #GPIO.setup(8,GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN)

def setTopLeft(channel):
    print("Player moved to space 1!")

def setTopRight(channel):
    print("Player moved to space 2!")

def setBotLeft(channel):
    print("Player moved to space 3")

def setBotRight(channel):
    print("Player moved to space 4!")


if __name__ == "__main__":
    matrixInit()
    #Initialize 2d array
    rows, cols = (2,2)
    gameBoard = [[0] * cols] * rows
    n = 0
    while(not GPIO.input(10)):
        time.sleep(0)