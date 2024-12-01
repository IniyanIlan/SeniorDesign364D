import sys
#import RPi.GPIO as GPIO
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

#for i in range(12):
#    print(lookUpTableHexagon[i])
#    print(len(lookUpTableHexagon[i]))

# Representation of the sensor matrix and its mapping to the hexagon matrix
lookUpTableSensors = [ [0]*5 for i in range(8)]
#print(lookUpTableSensors)
#lookUpTableSensors[0] = [Node()]


def sail():
    # Add code here that extracts details from request data flag
    # distance = diceData[0] real line, replace when done testing
    currentPlayer = 1
    players.append(player())
    #players[0].x = 
    global rowCount
    rowCount = 0
    # while rowCount < presentMatrix.shape[0]:
    #     time.sleep(0.2)
    #     countRow()

    #scanMatrix()

    #spots = countSpots()  # Initialize spots count
    #player = players[currentPlayer-1]
    distance = 11 # Hard-coded distance for now to verfiy it works
    #rowCount = 0
    print("Entered main while loop")
    # Scan each row to update the matrix
    #while rowCount < presentMatrix.shape[0]:
        #time.sleep(0.2)
        #countRow()
    # Board has been scanned. Check for valid change
    # Valid Change is confirmed by seeing if there are only 2 pieces, and that only one piece has moved (the correct player)
    #validMatrix, newPos = isValidMatrixStateSail(playerNum, player)
    validMatrix = True
    newPos = (2,1)
    if validMatrix:
        # Further check that it moved by a correct distance
        distanceMoved = getDistanceMoved(player, (2,1))
        if distanceMoved <= distance:
            print(f"Player {currentPlayer} moved correctly by exactly {distanceMoved} units.")
            player.x = newPos[0]
            player.y = newPos[1]
            # pastMatrix[:, :] = presentMatrix[:, :]
            # # ADD ANY EXTRA OUTPUT OPTIONS HERE
            # matrixDataReady[0] = 1
            # matrixDataReady[1] = player.playerNumber - 1
            # matrixDataReady[2] = player.x
            # matrixDataReady[3] = player.y
            # matrixRequest[0] = 0 # Turn off matrixRequest.
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


sail()