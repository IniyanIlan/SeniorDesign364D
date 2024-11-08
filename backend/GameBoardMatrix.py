import RPi.GPIO as GPIO
import time
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np


# Access the shared memory by name
shm_name = 'PresentMatrix'  # Replace with actual shm.name from main process
array_shape = (5, 8)  # Same shape as created initially
array_dtype = np.int8  # Same dtype as initially created

# Connect to the existing shared memory block
existing_shmMatrix = shared_memory.SharedMemory(name=shm_name)

# Create a 2D NumPy array using the existing shared memory
presentArray = np.ndarray(array_shape, dtype=array_dtype, buffer=existing_shmMatrix.buf)

# Access the shared memory by name
shm_name = 'PastMatrix'  # Replace with actual shm.name from main process
array_shape = (5, 8)  # Same shape as created initially
array_dtype = np.int8  # Same dtype as initially created

# Connect to the existing shared memory block
existing_shmPastxMatrix = shared_memory.SharedMemory(name=shm_name)

# Create a 2D NumPy array using the existing shared memory
pastMatrix = np.ndarray(array_shape, dtype=array_dtype, buffer=existing_shmMatrix.buf)


def matrixInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Set up selector bits for MUXes (Pins 8, 10, 12)
    GPIO.setup(8, GPIO.IN, GPIO.PUD_DOWN) # selector 1 (LSB)
    GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN) # Selector 2
    GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN) # Selector 3 (MSB)

    #Set MUX Output GPIOs (3,5,7,9,11)
    # SET HERE WHEN THE PCB GETS HERE PLS

    #GPIO.setup(8, GPIO.IN, GPIO.PUD_DOWN) # pos 4
    # Set edge detection functions
    # GPIO.add_event_detect(3, GPIO.FALLING, setTopLeft, 20)
    # GPIO.add_event_detect(5, GPIO.FALLING, setTopRight, 20)
    # GPIO.add_event_detect(7, GPIO.FALLING, setBotLeft, 20)
    # GPIO.add_event_detect(8, GPIO.FALLING, setBotRight, 20)
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