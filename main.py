from random import randint
import os

def intinputvalidate(prompt, lower, upper):
    while True:
        try:
            temp = int(input(prompt))
            if lower != -1 and upper != -1:
                if temp < lower or temp > upper:
                    1 / 0
                else:
                    return temp
            else:
                return temp
        except Exception:
            print("Invalid input")

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear') # Wipe terminal

players = []

while True:
    newplayername = input("Input player name: (Input '0' once all players are in or '-1' to reset all names)\n")
    if newplayername == '0':
        if len(players) >= 3:
            print(f"All {len(players)} players:")
            for name in players:
                print(name)
            allplayernamesconfirm = intinputvalidate("Is this all players? (1=Yes, 0=No, add more)\n", 0, 1)
            if allplayernamesconfirm:
                break
        else:
            print("You must have at least 3 players to play")
    elif newplayername == '-1':
        players = []
        print("All names reset, please input all player names again")
    else:
        print(f"Name: {newplayername}")
        playernameconfirm = intinputvalidate("Add name to player list? (1=Yes, 0=No)\n", 0, 1)
        if playernameconfirm:
            players.append(newplayername)