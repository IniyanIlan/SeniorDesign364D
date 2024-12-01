import sys
import RPi.GPIO as GPIO
import time
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np
import time as sleep
from collections import deque


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


class Node:
    mapping = None
    validHexagons = []
    nodeNumberHex = -1
    isHexNode = True
    def __init__(self, mapping, validHexagons=[], NodeNumberHex=-1, isHexNode=True):
        self.mapping = mapping
        self.validHexagons = validHexagons
        self.nodeNumberHex = NodeNumberHex
        self.isHexNode = isHexNode
    def __str__(self):
        return f"{self.nodeNumberHex}"
    def __repr__(self):
        if(self.nodeNumberHex < 10):
            return f" {self.nodeNumberHex}"
        else:
            return f"{self.nodeNumberHex}"
    
# Colors-- Their index represents the player number as well
playerColors = ['Red', 'Orange', 'Blue', 'Purple', 'Gold', 'Pink']


# This list is purely to reset all nodes once a search is completed
hexagonNodes = []

# Local variabales
players = []

playerNum = 2 # default player number

# Representation of the Hexagon game board and its mappings to the sensor matrix
lookUpTableHexagon = [ [0]*11 for i in range(12)]
#print(lookUpTableHexagon)
# Row 0
lookUpTableHexagon[0] = [0, 0, 0, 0, 0, Node(None, [1], 2), 0, 0, 0, 0, 0]
# Row 1
lookUpTableHexagon[1] = [0, 0, 0, 0, Node(None, [1], 1), 0, Node(None, [1], 3), 0, 0, 0, 0]
# Row 2
lookUpTableHexagon[2] = [0, 0, Node(None, [2], 4), 0, Node(None, [1,3], 6), 0, Node(None, [1, 4], 8), 0, Node(None, [5], 10), 0, 0]
# Row 3
lookUpTableHexagon[3] = [0, Node(None, [2], 12), 0, Node(None, [2, 3], 5), 0, Node(None, [3, 4], 7), 0, Node(None, [4, 5], 9), 0, Node(None, [5], 11), 0]
# Row 4
lookUpTableHexagon[4] = [0, Node(None, [2, 6], 19), 0, Node(None, [2, 3, 7], 13), 0, Node(None, [3, 4, 8], 15), 0, Node(None, [4, 9, 5], 18), 0, 0, 0] # Last node is purposefully crossed out
# Row 5
lookUpTableHexagon[5] = [0, 0, Node(None, [2, 6, 7], 20), 0, Node(None, [3, 7, 8], 14), 0, Node(None, [4, 8, 9], 16), 0, Node(None, [5, 9, 10], 17), 0, 0]
# Row 6
lookUpTableHexagon[6] = [0, 0, Node(None, [6, 7, 11], 27), 0, Node(None, [7, 8, 12], 21), 0, Node(None, [8, 9, 13], 23), 0, Node(None, [9, 10, 14], 25), 0, 0]
# Row 7
lookUpTableHexagon[7] = [0, 0, 0, Node(None, [7, 11, 12], 32), 0, Node(None, [8, 12, 13], 22), 0, Node(None, [9, 13, 14], 24), 0, Node(None, [9, 10, 14], 25), 0] # Node deleted here
# Row 8
lookUpTableHexagon[8] = [0, Node(None, [11], 39), 0, Node(None, [11, 12, 15], 33), 0, Node(None, [12, 13, 16], 28), 0, Node(None, [13, 14, 17], 30), 0, Node(None, [14], 40), 0]
# Row 9
lookUpTableHexagon[9] = [0, 0, Node(None, [11, 15], 38), 0, Node(None, [12, 15, 16], 34), 0, Node(None, [13, 16, 17], 29), 0, Node(None, [14, 17], 31), 0, 0]
# Row 10
lookUpTableHexagon[10] = [0, 0, 0, 0, Node(None, [15, 16], 37), 0, Node(None, [16, 17], 35), 0, 0, 0, 0]
# Row 11
lookUpTableHexagon[11] = [0, 0, 0, 0, 0, Node(None, [16], 36), 0, 0, 0, 0, 0]


# This list is purely to reset all nodes once a search is completed
hexagonNodes = []





# Representation of the sensor matrix and its mapping to the hexagon matrix
lookUpTableSensors = [ [0]*5 for i in range(8)]

## TODO: FILL OUT THE REST OF THIS WHEN PCB IS FULLY ASSEMBLED
# lookUpTableSensors[0] = [Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False)]
# lookUpTableSensors[1] = [Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False), Node(mapping= , isHexNode=False)]
# lookUpTableSensors[2] = [Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False)]
# lookUpTableSensors[3] = [Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False)]
# lookUpTableSensors[4] = [Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False)]
# lookUpTableSensors[5] = [Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False)]
# lookUpTableSensors[6] = [Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False)]
# lookUpTableSensors[7] = [Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False), Node(mapping= None, isHexNode=False)]



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
matrixDataReady = np.ndarray(6, dtype=np.int64, buffer=existingData.buf)
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
    GPIO.setup(8, GPIO.OUT, 0) # selector 1 (LSB)
    GPIO.setup(10, GPIO.OUT, 0) # Selector 2
    GPIO.setup(12, GPIO.OUT, 0) # Selector 3 (MSB)

    #Set MUX Output GPIOs (3,5,7,9,11)
    # SET HERE WHEN THE PCB GETS HERE PLS

    GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(9, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(11, GPIO.IN, GPIO.PUD_DOWN)

    # Demo code
    # Pin Init

    # GPIO.setup(15, GPIO.IN, GPIO.PUD_DOWN) #shutdown program pin
    # GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.setup(5, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.setup(11, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.setup(15, GPIO.IN, GPIO.PUD_DOWN)
    # GPIO.setup(19, GPIO.IN, GPIO.PUD_DOWN)



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


def countRow(row):
    # Set selector row
    match row:
        case 0:
            GPIO.output(12, 0)
            GPIO.output(10, 0)
            GPIO.output(8,  0)
        case 1:
            GPIO.output(12, 0)
            GPIO.output(10, 0)
            GPIO.output(8,  1)
        case 2:
            GPIO.output(12, 0)
            GPIO.output(10, 1)
            GPIO.output(8,  0)
        case 3:
            GPIO.output(12, 0)
            GPIO.output(10, 1)
            GPIO.output(8,  1)
        case 4:
            GPIO.output(12, 1)
            GPIO.output(10, 0)
            GPIO.output(8,  0)
        case 5:
            GPIO.output(12, 1)
            GPIO.output(10, 0)
            GPIO.output(8,  1)
        case 6:
            GPIO.output(12, 1)
            GPIO.output(10, 1)
            GPIO.output(8,  0)
        case 7:
            GPIO.output(12, 1)
            GPIO.output(10, 1)
            GPIO.output(8,  1)
    sleep(0.0001) # might need to wait a second since the propagation of the MUX might be slower than the clock speed
    presentMatrix[row][0] = GPIO.input(3)
    presentMatrix[row][1] = GPIO.input(5)
    presentMatrix[row][2] = GPIO.input(7)
    presentMatrix[row][3] = GPIO.input(9)
    presentMatrix[row][4] = GPIO.input(11)



    
    # global rowCount
    # if (rowCount == 0):
    #     presentMatrix[0][0] = 1 - GPIO.input(3)
    #     presentMatrix[0][1] = 1 - GPIO.input(5)
    # elif (rowCount == 1):
    #     presentMatrix[1][0] = 1 - GPIO.input(7)
    #     presentMatrix[1][1] = 1 - GPIO.input(11)
    # rowCount += 1
    return


def scanMatrix():
    for i in range(8):
        countRow(i)
        
        
    
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
    # while rowCount < presentMatrix.shape[0]:
    #     time.sleep(0.2)
    #     countRow()

    scanMatrix()

    spots = countSpots()  # Initialize spots count
    player = players[currentPlayer-1]
    distance = 2 # Hard-coded distance for now to verfiy it works
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
            print(f"Player {currentPlayer} moved correctly by exactly {distanceMoved} units.")
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

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 1),  # Top-right
        (-1, -1), # Top-left
        (1, -1),  # Bottom-left
        (1, 1)    # Bottom-right
    ]
        
    #hexagonEndPos = lookUpTableSensors[newPos[0]][newPos[1]].mapping
    #hexagonBeginPos = lookUpTableSensors[player.x][player.y].mapping
    hexagonBeginPos = (0, 5)
    hexagonEndPos = (7, 9)
    # BFS :)
    queue = deque([(hexagonBeginPos, 0)])  # (current_node, distance)
    visited = set()
    visited.add(hexagonBeginPos)

    while queue:
        (current_x, current_y), distance = queue.popleft()
        print(f"BFS is at Node {(current_x, current_y)}")
        # Check if we've reached the target node
        if (current_x, current_y) == hexagonEndPos:
            return distance

        # Check all valid neighbors
        for dx, dy in directions:
            neighbor_x, neighbor_y = current_x + dx, current_y + dy

            # Ensure the neighbor is within bounds and is a Node object
            if 0 <= neighbor_x < len(lookUpTableHexagon) and 0 <= neighbor_y < len(lookUpTableHexagon[0]):
                neighbor_node = lookUpTableHexagon[neighbor_x][neighbor_y]
                if neighbor_node and (neighbor_x, neighbor_y) not in visited:
                    queue.append(((neighbor_x, neighbor_y), distance + 1))
                    #print(f"Adding")
                    visited.add((neighbor_x, neighbor_y))

    return -1  # Target node is unreachable



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
            # Prepare data
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

