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

# Roles: 0 - Villager, 1 - Werewolf, 2 - Naughty Girl, 3 - Drunk, 4 - Hunter, 5 - Jester, 6 - Sheriff
rolenames = ["Villager", "Werewolf", "Naughty Girl", "Drunk", "Hunter", "Jester", "Sheriff"]

playerlist = []
roleslist = []

while True:
    newplayername = input("Input player name: (Input '0' once all players are in or '-1' to reset all names)\n")
    if newplayername == '0':
        if len(playerlist) >= 3:
            print(f"All {len(playerlist)} players:")
            for name in playerlist:
                print(name)
            allplayernamesconfirm = intinputvalidate("Is this all players? (1=Yes, 0=No, add more)\n", 0, 1)
            if allplayernamesconfirm:
                break
        else:
            print("You must have at least 3 players to play")
    elif newplayername == '-1':
        playerlist = []
        roleslist = []
        print("All names reset, please input all player names again")
    else:
        print(f"Name: {newplayername}")
        playernameconfirm = intinputvalidate("Add name to player list? (1=Yes, 0=No)\n", 0, 1)
        if playernameconfirm:
            playerlist.append(newplayername)
            roleslist.append(0)

playernum = len(playerlist)
werewolfnum = playernum // 4
if werewolfnum <= 0:
    werewolfnum = 1

werewolfidlist = []
for i in range(werewolfnum):
    while True:
        newwerewolfid = randint(0, playernum-1)
        if newwerewolfid not in werewolfidlist:
            werewolfidlist.append(newwerewolfid)
            break

for i in range(len(roleslist)):
    if i in werewolfidlist:
        roleslist[i] = 1
