import sys
import RPi.GPIO as GPIO
import time
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np


class player:
    x = 0
    y = 0
    playerNumber = 0
    def __init__(self):
        self.x = -1
        self.y = -1
        self.playerNumber = -1
    def __str__(self):
        return "Player Number: " + str(self.playerNumber) + " is at Position: (" + str(self.x) + ", " + str(self.y) + ")"



players = []

playerNum = 2 # default player number

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
matrixRequest = np.ndarray(2, dtype=np.int64, buffer=existingRequest.buf)
matrixDataReady = np.ndarray(4, dtype=np.int64, buffer=existingData.buf)
existingDiceData = shared_memory.SharedMemory(name='DiceData')
diceData = np.ndarray(1, dtype=np.int8, buffer=existingDiceData.buf)

# FOR TESTING MODULE ONLY
# Initialize 2x2 matrices with zeros
# pastMatrix = np.zeros((2, 2), dtype=int)
# presentMatrix = np.zeros((2, 2), dtype=int)
# pastMatrix[:, :] = 0
# presentMatrix[:, :] = 0


#Variables
rowCount = 0


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
    GPIO.setup(19, GPIO.IN, GPIO.PUD_DOWN)



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
    global rowCount
    if (rowCount == 0):
        presentMatrix[0][0] = 1 - GPIO.input(3)
        presentMatrix[0][1] = 1 - GPIO.input(5)
    elif (rowCount == 1):
        presentMatrix[1][0] = 1 - GPIO.input(7)
        presentMatrix[1][1] = 1 - GPIO.input(11)
    rowCount += 1
    return




def countSpots():
    playerSpots = 0
    for i, row in enumerate(presentMatrix):
        for j, element in enumerate(row):
            if element == 1:
                playerSpots += 1
    print(f"Found {playerSpots} spots")
    return playerSpots


def sail(currentPlayer):
    # Add code here that extracts details from request data flag
    # distance = diceData[0] real line, replace when done testing
    global rowCount
    rowCount = 0
    while rowCount < presentMatrix.shape[0]:
        time.sleep(0.2)
        countRow()
    spots = countSpots()  # Initialize spots count
    player = players[currentPlayer-1]
    distance = 2 # Hard-coded distance for now to verfiy it works
    while spots < playerNum:
        rowCount = 0
        print("Entered main while loop")
        # Scan each row to update the matrix
        while rowCount < presentMatrix.shape[0]:
            time.sleep(0.2)
            countRow()
        # Board has been scanned. Check for valid change
        # Valid Change is confirmed by seeing if there are only 2 pieces, and that only one piece has moved (the correct player)
        validMatrix, newPos = isValidMatrixStateSail(playerNum, player)
        if validMatrix:
            # Further check that it moved by a correct distance
            distanceMoved = getDistanceMoved(player, newPos)
            if distanceMoved <= distance:
                print(f"Player {currentPlayer} moved correctly by {distanceMoved} units.")
                player.x = newPos[0]
                player.y = newPos[1]
                pastMatrix[:, :] = presentMatrix[:, :]
                # ADD ANY EXTRA OUTPUT OPTIONS HERE
                matrixDataReady[0] = 1
                matrixDataReady[1] = player.playerNumber - 1
                matrixDataReady[2] = player.x
                matrixDataReady[3] = player.y
                matrixRequest[0] = 0 # Turn off matrixRequest.
                return
            else:
                print(f"Player {currentPlayer} movement invalid. Expected {distance} units but moved {distanceMoved} units.")
        else:
            print(f"Invalid matrix state for player {currentPlayer}. Retrying.")
    # Update pastMatrix with the new state for the next check


def getDistanceMoved(player, newPos):
    if(newPos == (player.x, player.y)):
        return 0 # No pieces moved. We can assume nothing happened
    # Find the player’s current position in the matrix
    initial_pos = (player.x, player.y)  # Assuming each player has a previous position
    
    distance_moved = abs(newPos[0] - initial_pos[0]) + abs(newPos[1] - initial_pos[1])
    
    return distance_moved



# Waits for player input to place a piece down on the board. Must be a location that is valid (the edge of the board)
# If the placement is valid, a new player object is instantiated with the coordinate of that spot, and added
# To the player list.
def setPlayers(playerNum):
    global rowCount
    spots = countSpots()  # Initialize spots count
    playersToPlace = 1
    for i in range(playerNum):
    # Loop until we have the required number of valid player placements
        while spots < playerNum:
            rowCount = 0
            # Scan each row to update the matrix (assumes a 2x2 matrix for testing)
            while rowCount < presentMatrix.shape[0]:
                time.sleep(0.2)
                countRow()
            print(presentMatrix)
            # Check if the current matrix state is valid with expected spots = playerNum
            if isValidMatrixStateSetup(playersToPlace):
                # Identify new player position by comparing present and past matrices
                changed_positions = []
                for i in range(presentMatrix.shape[0]):
                    for j in range(presentMatrix.shape[1]):
                        if presentMatrix[i][j] != pastMatrix[i][j]:
                            changed_positions.append((i, j))
                            changed_positions.append((i, j))

                if len(changed_positions) == 2:
                    (old_x, old_y), (new_x, new_y) = changed_positions
                    if pastMatrix[old_x][old_y] == 0 and presentMatrix[new_x][new_y] == 1:
                        # Valid new player placement
                        new_player = player()
                        new_player.x, new_player.y = new_x, new_y
                        players.append(new_player)
                        new_player.playerNumber = len(players)
                        print(f"New player added at ({new_x}, {new_y})")
                    
                        # Update the pastMatrix for the next scan
                        pastMatrix[:, :] = presentMatrix[:, :]

                        # Update spots count
                        spots = countSpots()
                        playersToPlace += 1
                    else:
                        print("Invalid movement detected.")
                else:
                    print("Invalid player placement; retrying.")
            else:
                print("Matrix state is invalid; retrying.")

        print(f"All {playerNum} players successfully placed.")
        matrixDataReady[0] = 1
        matrixRequest[0] = 0 # Turn off matrixRequest.

            
        

    


def attack(playerNum):
    attackingPlayer = players[playerNum-1] # Assuming players are 1-indexed
    # Clear player matrixDataReady stuff
    matrixDataReady[1] = 0
    # This just checks for a valid state in the pastMatrix for the player
    # If a player is nearby another player, attack is valid
    
    # Iterate over each player to check for nearby players within a 1-tile range
    for player in players:
        # Skip if the player is the same as the attacker
        if player == attackingPlayer:
            continue
        
        # Check if the player is within attack range (1 tile in any direction)
        if abs(player.x - attackingPlayer.x) <= 1 and abs(player.y - attackingPlayer.y) <= 1:
            # If within range, the attack is considered valid for this player
            print(f"{attackingPlayer} can attack {player}")
            # Perform any additional actions for an attack (e.g., reduce health)
            matrixDataReady[1] *= 10
            matrixDataReady[1] += player.playerNumber # store player Number
    if(matrixDataReady[1] == 0): 
        matrixDataReady[0] = -1 # No players were found. Invalid data
    else:
        matrixDataReady[0] = 2 # Valid attck
    matrixRequest[0] = 0 # Turn off matrixRequest.



def excavate():
    # Valid return code if the player is nearby a treasure chest
    matrixDataReady[0] = 1 # treasure chest always found for now
    matrixRequest[0] = 0 # Turn off matrixRequest.
    return

# USED DURING PLAYER LOCATION SETUP
def isValidMatrixStateSetup(expected_num_players):
    # Count the number of spots (1s) in the present matrix
    playerSpots = countSpots()
    
    # Check if the number of player spots matches the expected count
    if playerSpots != expected_num_players:
        print(f"Invalid number of players: expected {expected_num_players}, found {playerSpots}")
        return False
    
    # Check for single movement by comparing present and past matrices
    changed_positions = []
    rows, cols = pastMatrix.shape
    for i in range(rows):
        for j in range(cols):
            if presentMatrix[i][j] != pastMatrix[i][j]:
                changed_positions.append((i, j))
                changed_positions.append((i, j))
    print(len(changed_positions))
    # Valid movement occurs if there is exactly one changed position
    # (one cell went from 0 to 1)
    if len(changed_positions) == 2:
        (old_x, old_y), (new_x, new_y) = changed_positions
        if pastMatrix[old_x][old_y] == 0 and presentMatrix[new_x][new_y] == 1:
            # Valid move detected
            print("Valid move detected: single player moved.")
            return True
        else:
            print("Detected multiple or invalid changes.")
            return False
    elif len(changed_positions) == 0:
        # No movement detected, but the state is valid
        print("No movement detected, state is valid.")
        return True
    else:
        # Invalid move if there are more or fewer than two changes
        print("Invalid move: multiple or no changes detected.")
        return False

# USED DURING PLAYER MOVEMENT/SAILING
def isValidMatrixStateSail(expected_num_players, currentPlayer):
    # Count the number of spots (1s) in the present matrix
    playerSpots = countSpots()
    
    # Check if the number of player spots matches the expected count
    if playerSpots != expected_num_players:
        print(f"Invalid number of players: expected {expected_num_players}, found {playerSpots}")
        return False, (-1, -1)
    
    # Check for single movement by comparing present and past matrices
    changed_positions = []
    rows, cols = pastMatrix.shape
    for i in range(rows):
        for j in range(cols):
            if presentMatrix[i][j] != pastMatrix[i][j]:
                changed_positions.append((i, j))
    print(changed_positions)
    # Valid movement occurs if there are exactly two changed positions
    # (one cell went from 1 to 0 and another from 0 to 1)
    if len(changed_positions) == 2:
        if changed_positions[0] == (player.x, player.y):
            (old_x, old_y), (new_x, new_y) = changed_positions
        else:
            (new_x, new_y), (old_x, old_y) = changed_positions
        if presentMatrix[old_x][old_y] == 0 and presentMatrix[new_x][new_y] == 1 and pastMatrix[old_x][old_y] == 1:
            # Valid move detected
            print("Valid move detected: single player moved.")
            return True, (new_x, new_y)
        else:
            print("Detected multiple or invalid changes.")
            return False, (-1, -1)
    elif len(changed_positions) == 0:
        # No movement detected, but the state is valid
        print("No movement detected, state is valid.")
        return True, (currentPlayer.x, currentPlayer.y)
    else:
        # Invalid move if there are more or fewer than two changes
        print("Invalid move: multiple or no changes detected.")
        return False, (-1, -1)


if __name__ == "__main__":
    try:
        print("shared memory initialized correctly")
        matrixInit()
        while(not GPIO.input(15)): # This is just an exit program condition. Dont worry about it
            if((matrixRequest[0] == 1)): # 1 = sail
                sail(matrixRequest[1]) # Index 1 corresponds to which player is the one choosing to do this (player turn)
            elif(matrixRequest[0] == 2): # 2 = attack
                attack(matrixRequest[1])
            elif(matrixRequest[0] == 3): # 3 = excavate
                excavate(matrixRequest[1])
            elif(matrixRequest[0] == 4): # 4 = Player position initialization
                setPlayers(playerNum)
                for player in players:
                    print(player)
            
            
        # while(not GPIO.input(15)):
        #     if(GPIO.input(19)):
        #         attack(playerNum) # Hard-coded to only be 1's turn. Obviously will be different afterwards
        #         for player in players:
        #             print(player)
        #     # elif((matrixRequest[0] % 10) == 2):
        #     #     attack(matrixRequest[0] / 10)
        #     # elif((matrixRequest[0] % 10) == 3):
        #     #     excavate(matrixRequest[0] / 10)
        #     # elif((matrixRequest[0] % 10) == 4):
        #     #     setPlayers(playerNum)
        #     # Scan matrix for spots
        #     #spots = countSpots()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('Exited')

