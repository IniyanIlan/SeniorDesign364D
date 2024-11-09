import RPi.GPIO as GPIO
import time
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np

class player:
    x = 0
    y = 0
    def __init__(self):
        self.x = -1
        self.y = -1


player1 = player()
player2 = player()
player3 = player()
player4 = player()


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
existingDiceData = shared_memory.SharedMemory(name='DiceData')
diceData = np.ndarray(1, dtype=np.int8, buffer=existingDiceData.buf)


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




def countSpots():
    playerSpots = 0
    for i, row in enumerate(presentMatrix):
        for j, element in enumerate(row):
            if element == 1:
                playerSpots += 1
    return spots


def walk(currentPlayer):
    # Add code here that extracts details from request data flag
    distance = diceData[0]
    while(row < 2):
        countRow()
    row = 0
    
    # Board has been scanned. Check for valid change
    # Valid Change is confirmed by seeing if there are only 2 pieces, and that only one piece has moved (the correct player)
    spots = countSpots
    if(spots != 2): # invalid number of players. 
        return # try again on the next loop
    # Now check if only one player has moved
    # Find the difference between present and past matrices to detect movement
    changed_positions = []
    for i in range(array_shape[0]):
        for j in range(array_shape[1]):
            if presentMatrix[i][j] != pastMatrix[i][j]:
                changed_positions.append((i, j))

    # Valid change occurs if exactly one piece moved, resulting in exactly two changes
    # (one position went from 1 to 0, another from 0 to 1)
    if len(changed_positions) != 2:
        print("Invalid move: multiple or no changes detected.")
        return  # Retry on the next scan

    # Check that only one player's position has changed
    (old_x, old_y), (new_x, new_y) = changed_positions
    if presentMatrix[old_x][old_y] == 0 and presentMatrix[new_x][new_y] == 1:
        # Update currentPlayer position in the player instance
        currentPlayer.x, currentPlayer.y = new_x, new_y
        print(f"Player {currentPlayer} moved to ({new_x}, {new_y})")

    # Update pastMatrix with the new state for the next check
    pastMatrix[:, :] = presentMatrix[:, :]


    


def attack():
    countRow()

def excavate():
    countRow()


if __name__ == "__main__":
    matrixInit()
    while(not GPIO.input(15)):
        if((matrixRequest[0] % 10) == 1):
            walk(matrixRequest[0] / 10)
        elif((matrixRequest[0] % 10) == 2):
            attack(matrixRequest[0] / 10)
        elif((matrixRequest[0] % 10) == 3):
            excavate(matrixRequest[0] / 10)
        # Scan matrix for spots
        spots = countSpots()
        time.sleep(0.01)

