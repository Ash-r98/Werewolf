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

# Subroutines

def die(playerid):
    print(f"Player {playerlist[playerid]} has died. They were a {rolenames[roleslist[playerid]]}")
    living[playerid] = False
    if roleslist[playerid] == 4:
        hunterdeathact(playerid)

def playerselectnotself(playerid):
    selectid = 0 # Placeholder in case of error

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

def playerselectwithself():
    selectid = 0 # Placeholder in case of error

    while True:
        flag = False
        otherflag = False
        selectname = input("Input the name of the player you would like to select: (leave empty to display all player names)\n")
        if selectname == '':
            displaynames()
        else:
            for i in range(len(playerlist)):
                if playerlist[i] == selectname:
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

def checkwin():
    aliveplayersnum = 0
    alivewerewolvesnum = 0

    for life in living:
        if life:
            aliveplayersnum += 1

    for i in range(len(roleslist)):
        if roleslist[i] == 1:
            if living[i]:
                alivewerewolvesnum += 1

    anywin = False # If true, either villagers or werewolves have won
    winid = 0 # 0 = No win, 1 = Villagers, 2 = Werewolves

    if alivewerewolvesnum <= 0:
        anywin = True
        winid = 1
    elif aliveplayersnum / 2 <= alivewerewolvesnum:
        anywin = True
        winid = 2
    # If neither if statement hits, then neither side has won and the game will continue

    return anywin, winid

def privateplayerchoiceprep(playerid):
    playername = playerlist[playerid]
    print(f"Pass the device to player {playername}")
    sleep(1)

    input(f"Player {playername}, press enter when you are ready\n")

    print(f"\033[31mALL PLAYERS EXCEPT PLAYER {playername} LOOK AWAY\033[0m")
    print("3", end="\r")
    sleep(1)
    print("2", end="\r")
    sleep(1)
    print("1", end="\r")
    sleep(1)


# Character Actions

def villageract():
    print("You will be asked to input two players' names to disguise your role")
    for i in range(2):
        villagercode = playerlist[randint(0, playernum-1)]
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
    print(f"Player {playerlist[deadplayer]} has been killed by the werewolves. They were a {rolenames[roleslist[deadplayer]]}")
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
    print(f"You chose to kill player {playerlist[select]}")
    die(select)


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
            select = playerid # Returns the sheriff as the dead player

    return killconfirm, hit, select

def vote(playerid):
    if roleslist[playerid] != 1 and roleslist[playerid] != 5:
        print("You must select a player to vote who you think is a werewolf. Remember, if a jester is voted out then they will win")
    elif roleslist[playerid] == 1:
        print("You must vote someone out of the game, votes are private so don't vote for another werewolf. Remember, if a jester is voted out then they will win")
    else:
        print("You are the jester, so if you get voted out you will win. Voting yourself is likely the best option here, however you are allowed to vote for anyone")

    votedplayer = playerselectwithself()
    return votedplayer


# Game Loop

night = 0
jesterwin = False
run = True
while run:
    night += 1 # Increments night counter at the start of the game loop, starting at 1

    sheriffresult = [False, False, -1] # Resets sheriff result at the start of the game loop
    roleslistnightcopy = roleslist # Copy of roleslist for this night that won't be changed when roles are swapped around

    for i in range(playernum):
        playername = playerlist[i] # For easy use in the for loop

        # Night number stays at top for the whole night
        clearscreen()
        print(f"Night {night}\n")
        sleep(1)

        if living[i]:
            privateplayerchoiceprep(i)

            print(f"Player {playername}, you are a {rolenames[roleslist[i]]}")
            sleep(1)
            match roleslistnightcopy[i]:
                case 0:
                    villageract()
                case 1:
                    # Displays all werewolf allies
                    allylist = []
                    for j in range(len(roleslist)):
                        if j != i:
                            if roleslist[j] == 1:
                                allylist.append(playerlist[j])
                    if len(allylist) > 0:
                        print("The other werewolves are:")
                        for ally in allylist:
                            print(ally)

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

        sleep(3)

    # End of night

    clearscreen()
    print(f"Day {night}\n") # Night counter = Day counter
    sleep(1)

    print("The night has ended, and the players have woken up")
    sleep(1)

    # Werewolf kill
    werewolfkill()
    sleep(1)

    # Possible sheriff kill
    if sheriffresult[0]: # If the sheriff attempted to kill someone
        if sheriffresult[1]: # If the sheriff correctly killed a werewolf or jester
            print(f"The sheriff correctly killed player {playerlist[sheriffresult[2]]}")
            die(sheriffresult[2])
        else: # The sheriff incorrectly shot and killed themselves
            print(f"The sheriff {playerlist[sheriffresult[2]]} attempted to shoot an innocent and instead killed themself")
            die(sheriffresult[2])
        sleep(1)

    checkwinresult = checkwin()
    if checkwinresult[0]: # If there has been a win, exit the game loop
        run = False
    else: # Otherwise, the players will vote someone out
        print("It is time to vote a player out. Discuss amongst yourselves who you want to vote")
        sleep(1)
        input("Press enter when everyone is ready to vote\n")

        votelist = []
        for i in range(playernum):
            clearscreen()
            print(f"Day {night}\n")  # Night counter = Day counter
            sleep(1)

            if living[i]:
                privateplayerchoiceprep(i)

                playervote = vote(i)

                voteflag = True
                for j in range(len(votelist)):
                    if votelist[j][0] == playervote:
                        votelist[j][1] += 1
                        voteflag = False
                if voteflag: # If vote not already in list
                    votelist.append([playervote, 1])

            else:
                print(f"Player {playerlist[i]} is dead")
                sleep(2)

        clearscreen()
        print(f"Day {night}\n")  # Night counter = Day counter
        sleep(1)
        print("Every player has voted\n")
        sleep(1)

        maxvotenum = 0
        votedplayerlist = []
        for i in range(len(votelist)):
            if votelist[i][1] > maxvotenum: # If strictly higher than max
                maxvotenum = votelist[i][1]
                votedplayerlist = [votelist[i][0]]
            elif votelist[i][1] == maxvotenum: # If equal to max
                votedplayerlist.append(votelist[i][0])
            # Otherwise the index can be ignored

        if len(votedplayerlist) == 1: # If one player had the most votes
            votedplayer = votedplayerlist[0]
            print(f"Player {playerlist[votedplayer]} was voted out.")
            die(votedplayer)
            if roleslist[votedplayer] == 5:
                jesterwin = True
                run = False
        else: # In case of a tie
            print(f"There was a tie in votes between {len(votedplayerlist)} players:")
            for name in votedplayerlist:
                print(name)
            print("Because there was a tie in votes, no one will be removed from the game")

        checkwinresult = checkwin()
        if checkwinresult[0]:
            run = False

        sleep(3)


if not jesterwin:
    if checkwinresult[1] == 1:
        print("The villagers have won!")
    elif checkwinresult[1] == 2:
        print("The werewolves have won!")
else:
    print("The jester has won!")

sleep(5)