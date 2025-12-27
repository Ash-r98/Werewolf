from time import sleep
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
living = []
nameconfirmation = False

def displaynames():
    print(f"All {len(playerlist)} players:")
    for name in playerlist:
        print(name)
    print() # Leaves whitespace after names are displayed

while True:
    newplayername = input("Input player name: (Input '0' once all players are in or '-1' to reset all names)\n")
    if newplayername == '0':
        if len(playerlist) >= 3:
            displaynames()
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
        if newplayername not in playerlist:
            print(f"Name: {newplayername}")
            if nameconfirmation:
                playernameconfirm = intinputvalidate("Add name to player list? (1=Yes, 0=No)\n", 0, 1)
            else:
                playernameconfirm = True
            if playernameconfirm:
                playerlist.append(newplayername)
                roleslist.append(0)
                living.append(True)
        else:
            print("Name is already taken")

# Roles setup

playernum = len(playerlist)
werewolfnum = playernum // 4
if werewolfnum <= 0:
    werewolfnum = 1

# Werewolf setup

werewolfkillvotes = []

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

# Other roles

otherroleslist = [0, 0, 2, 3, 4, 5, 6]
if playernum - werewolfnum > 7:
    for i in range(playernum - werewolfnum - 7):
        otherroleslist.append(0)  # Adds a villager for each extra player

for i in range(len(roleslist)):
    if roleslist[i] == 1:
        continue
    else:
        roleslist[i] = otherroleslist.pop(randint(0, len(otherroleslist) - 1))



print("\nAll roles have been allocated.")
sleep(3)
clearscreen()

night = 1

# Character Actions

def playerselectnotself(playerid):
    while True:
        flag = False
        otherflag = False
        selectname = input("Input the name of the player you would like to select: (leave empty to display all player names)\n")
        if selectname == '':
            displaynames()
        else:
            for i in range(len(playerlist)):
                if playerlist[i] == selectname:
                    if i == playerid:
                        print("You can't select yourself")
                        otherflag = True
                    else:
                        if not living[i]:
                            print(f"Player {selectname} is dead, you can't select them")
                            otherflag = True
                        else:
                            selectid = i
                            flag = True
            if flag:
                break
            elif not otherflag:
                print("Player not found")
    return selectid

def villageract():
    print("You will be asked to input two players' names to disguise your role")
    for i in range(2):
        villagercode = playerlist[randint(0, playernum)]
        while True:
            cmd = input(f"Input the name '{villagercode}'\n")
            if cmd == villagercode:
                break
            else:
                print("Incorrect input")


def werewolfact(playerid):
    print("You must select a player to vote to kill them. One of the voted players will be killed at random")

    for i in range(len(werewolfkillvotes)):
        print(f"Werewolf {i+1} voted to kill {playerlist[werewolfkillvotes[i]]}")

    killvote = playerselectnotself(playerid)
    werewolfkillvotes.append(killvote)

def werewolfkill():
    deadplayer = werewolfkillvotes[randint(0, len(werewolfkillvotes)-1)]
    print(f"Player {playerlist[deadplayer]} has been killed")
    living[deadplayer] = False


def naughtygirlact(playerid):
    print("You will select two other players (not yourself) and swap their roles")
    select1 = playerselectnotself(playerid)
    while True:
        select2 = playerselectnotself(playerid)
        if select2 != select1:
            break
        else:
            print("You can't select the same player again")

    roleslist[select1], roleslist[select2] = roleslist[select2], roleslist[select1]


def drunkact(playerid):
    print("You will select another player and swap your own role with theirs")
    select = playerselectnotself(playerid)

    roleslist[playerid], roleslist[select] = roleslist[select], roleslist[playerid]


def hunterdeathact(playerid):
    print("The Hunter has died, and can now select a player to kill")
    select = playerselectnotself(playerid)
    print(f"Player {playerlist[select]} has been killed")
    living[select] = False


def sheriffact(playerid):
    # Placeholder values for return with no action
    hit = False
    select = -1

    print("You are the sheriff, and can choose a player to kill, but if you select an innocent you will die instead")
    killconfirm = intinputvalidate("Would you like to try to kill someone tonight? (1=Yes, 0=No)\n", 0, 1)
    if killconfirm:
        select = playerselectnotself(playerid)
        if roleslist[select] == 1 or roleslist[select] == 5: # Hit
            living[select] = False
            hit = True
        else: # Miss
            living[playerid] = False

    return killconfirm, hit, select


# Game Loop

night = 0
run = True
while run:
    night += 1 # Increments night counter at the start of the game loop, starting at 1

    sheriffresult = [False, False, -1] # Resets sheriff result at the start of the game loop

    for i in range(playernum):
        playername = playerlist[i] # For easy use in the for loop

        # Night number stays at top for the whole night
        clearscreen()
        print(f"Night {night}")
        sleep(1)

        if living[i]:
            print(f"Pass the device to player {playername}")
            sleep(1)

            input(f"Player {playername}, press enter when you are ready")

            print(f"\033[31mALL PLAYERS EXCEPT PLAYER {playername} LOOK AWAY\033[0m")
            print("3", end="\r")
            sleep(1)
            print("2", end="\r")
            sleep(1)
            print("1", end="\r")
            sleep(1)

            print(f"Player {playername}, you are a {rolenames[roleslist[i]]}")
            sleep(1)
            match roleslist[i]:
                case 0:
                    villageract()
                case 1:
                    werewolfact(i)
                case 2:
                    naughtygirlact(i)
                case 3:
                    drunkact(i)
                case 4:
                    print("When you die, you will be able to kill a player of your choice. Try to kill a werewolf")
                case 5:
                    print("Your goal is to be voted out by the other players. If this happens you will win, but if you are killed then you lose")
                case 6:
                    sheriffresult = sheriffact(i)
                case _:
                    print("Role not found")

        else:
            print(f"Player {playername} is dead.")
