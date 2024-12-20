import random
import math

#NEED: # of players

num_players = 6 #change this whenever we get information from SettingUp
chest_list = []
chest_locations = []
random.seed(None) # randomness on system entropy (makes it more random)


def initialize_chests():
    global chest_list
    chest_list = []  # Reset chest list
    # number of available chests is 1.5 times the number of players
    num_chests = 24
    for i in range(math.ceil(num_chests*0.65)):  
        chest_list.append(0)  # 0 for treasure
        num_chests = num_chests - 1
    for i in range(num_chests):
        chest_list.append(1)  # 1 for trap
        
def get_locations():
    chest_locations.clear()
    num_chests = 24
    for i in range(1, 20):
        rand_val = random.randint(0, 3)
        if num_chests > rand_val:
            num_chests -= rand_val
            chest_locations.append(rand_val)
        else:
            chest_locations.append(num_chests)
            num_chests = 0
    random.shuffle(chest_locations)
    return chest_locations

def get_locations():
    chest_locations.clear()
    num_chests = 24
    for i in range(1, 20):
        rand_val = random.randint(0, 3)
        if num_chests >= rand_val:
            num_chests -= rand_val
            chest_locations.append(rand_val)
        else:
            chest_locations.append(num_chests)
            num_chests -= num_chests
    return chest_locations

def get_chest_list():
    return chest_list

# EXCAVATION
# set number of treasure chests: create list to keep track of number of chests 
# generate random number to pick a random index of the list 
def excavate():
    if len(chest_list) == 0:
        print("No more chests to excavate!")
        return -1
    random.shuffle(chest_list)  
    result = chest_list.pop() 
    if result == 0:
        print("You found a treasure!")
    else:
        print("You fell into a trap!")
    return result

# ATTACK
# def attack():
#     your_roll = random.randint(0, 20) # placeholder for until we get dice reader input
#     their_roll = random.randint(0, 20) # placeholder for until we get dice reader input
#     print(your_roll)
#     print(their_roll)
#     if your_roll > their_roll:
#         return 0
#     else:
#         return 1
def attack(player1_roll, player2_roll):
    difference = player1_roll - player2_roll
    return difference * 75
    

def main():
    print("main")
 
if __name__ == "__main__":
    main()