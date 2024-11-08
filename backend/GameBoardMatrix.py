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
presentMatrix = np.ndarray(array_shape, dtype=array_dtype, buffer=existing_shmMatrix.buf)

# Access the shared memory by name
shm_name = 'PastMatrix'  # Replace with actual shm.name from main process
array_shape = (5, 8)  # Same shape as created initially
array_dtype = np.int8  # Same dtype as initially created

# Connect to the existing shared memory block
existing_shmPastxMatrix = shared_memory.SharedMemory(name=shm_name)

# Create a 2D NumPy array using the existing shared memory
pastMatrix = np.ndarray(array_shape, dtype=array_dtype, buffer=existing_shmMatrix.buf)

# Get Data Request/Ready values
existingRequest = shared_memory.SharedMemory(name='MatrixRequest')
existingData = shared_memory.SharedMemory(name='MatrixDataReady')
matrixRequest = np.ndarray(1, dtype=np.int8, buffer=existingRequest.buf)
matrixDataReady = np.ndarray(1, dtype=np.int8, buffer=existingData.buf)


#Variables
row = 0


def matrixInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Set up selector bits for MUXes (Pins 8, 10, 12)
    GPIO.setup(8, GPIO.IN, GPIO.PUD_DOWN) # selector 1 (LSB)
    GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN) # Selector 2
    GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN) # Selector 3 (MSB)

    #Set MUX Output GPIOs (3,5,7,9,11)
    # SET HERE WHEN THE PCB GETS HERE PLS
    ''' 
    
    
    '''
    # Demo code
    # Pin Init
    GPIO.setup(15, GPIO.IN, GPIO.PUD_DOWN) #shutdown program pin
    GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(11, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(15, GPIO.IN, GPIO.PUD_DOWN)


#     # Set edge detection functions
#     GPIO.add_event_detect(3, GPIO.FALLING, setTopLeft, 20)
#     GPIO.add_event_detect(5, GPIO.FALLING, setTopRight, 20)
#     GPIO.add_event_detect(7, GPIO.FALLING, setBotLeft, 20)
#     GPIO.add_event_detect(11, GPIO.FALLING, setBotRight, 20)   
#     #GPIO.setup(8,GPIO.OUT, initial=GPIO.LOW)
#     GPIO.setup(10, GPIO.IN, GPIO.PUD_DOWN)

# def setTopLeft(channel):
#     presentArray[0][0] = 1
#     print("Player moved to space 1!")


# def setTopRight(channel):
#     print("Player moved to space 2!")

# def setBotLeft(channel):
#     print("Player moved to space 3")

# def setBotRight(channel):
#     print("Player moved to space 4!")


def countRow():
    if row is 0:
        presentMatrix[0][0] = GPIO.input(3)
        presentMatrix[0][1] = GPIO.input(5)
    elif row is 1:
        presentMatrix[1][0] = GPIO.input(7)
        presentMatrix[1][1] = GPIO.input(11)
    row += 1
    if(row > 1):
        row = 0




def countSpots():
    playerSpots = 0
    
    return spots

def walk():
    countRow()

def attack():
    countRow()


def excavate():
    countRow()


if __name__ == "__main__":
    matrixInit()
    while(not GPIO.input(15)):
        if(matrixRequest[0] == 1):
            walk()
        elif(matrixRequest[0] == 2):
            attack()
        elif(matrixRequest[0] == 3):
            excavate()
        # Scan matrix for spots
        spots = countSpots()
        time.sleep(0.01)