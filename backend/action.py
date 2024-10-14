import random
import math

#NEED: # of players

num_players = 6 #change this whenever we get information from SettingUp
chest_list = []

def initialize_chests():
    # number of available chests is 1.5 the number of players
    for i in range(math.ceil(num_players * 1.5) / 2):
        # 0 for treausre
        # 1 for trap
        chest_list.append(0)
        chest_list.append(1)

# EXCAVATION
# set number of treasure chests: create list to keep track of number of chests 
# generate random number to pick a random index of the list 
def excavate():
    idx = random.randint(0, len(chest_list) - 1)
    result = chest_list[idx]
    chest_list.pop(idx)
    return result

# ATTACK
def attack():
    your_roll = random.randint(0, 20) # placeholder for until we get dice reader input
    their_roll = random.randint(0, 20) # placeholder for until we get dice reader input
    if your_roll > their_roll:
        return 0
    else:
        return 1