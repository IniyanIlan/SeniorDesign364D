import random
import math

#NEED: # of players

num_players = 6 #change this whenever we get information from SettingUp
chest_list = []


def initialize_chests():
    global chest_list
    chest_list = []  # Reset chest list
    # number of available chests is 1.5 times the number of players
    num_chests = math.ceil(num_players * 1.5)
    for i in range(num_chests // 2):  # Dividing by 2 to account for pairs (treasure, trap)
        chest_list.append(0)  # 0 for treasure
        chest_list.append(1)  # 1 for trap

def get_chest_list():
    return chest_list

# EXCAVATION
# set number of treasure chests: create list to keep track of number of chests 
# generate random number to pick a random index of the list 
def excavate():
    if len(chest_list) == 0:
        print("No more chests to excavate!")
        return -1
    idx = random.randint(0, len(chest_list) - 1)
    result = chest_list[idx]
    chest_list.pop(idx)
    if result == 0:
        print("You found a treasure!")
    else:
        print("You fell into a trap!")
    return result

# ATTACK
def attack():
    your_roll = random.randint(0, 20) # placeholder for until we get dice reader input
    their_roll = random.randint(0, 20) # placeholder for until we get dice reader input
    print(your_roll)
    print(their_roll)
    if your_roll > their_roll:
        return 0
    else:
        return 1
    

def main():
    initialize_chests()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    excavate()
    print(chest_list)
    attack()

if __name__ == "__main__":
    main()