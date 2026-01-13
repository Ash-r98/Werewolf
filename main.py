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

class Player:
    def __init__(self, newplayerid, newname, newroleid):
        # Object creation values
        self.playerid = newplayerid # ID in playerlist
        self.name = newname
        self.roleid = newroleid

        # Universal attributes
        self.living = True
        self.protected = False # Protection from death, reset at the start of each night

        # Survivor attribute
        self.survivorprotectavailable = True # Does the survivor still have their one time protect

        # Guardian Angel attributes
        self.guardianangelprotectavailable = True # Does the guardian angel still have their one time protect
        self.guardianangelprotectingid = None # If role is guardian angel, this is the id of person you are protecting
        self.guardian = False # If you have a guardian angel protecting you then True

        # Guesser wolf attributes
        self.doubleshotavailable = True

    def die(self):
        self.living = False
        if self.roleid == 0 or self.roleid in evilrolelist: # Can be multiple villagers/werewolves
            print(f"Player {self.name} has died. They were a {rolenames[self.roleid]}")
        else: # Only one of each other role
            print(f"Player {self.name} has died. They were the {rolenames[self.roleid]}")
        if self.roleid == 4:
            hunterdeathact(self.playerid)

# Roles: 0 - Villager, 1 - Werewolf, 2 - Naughty Girl, 3 - Drunk, 4 - Hunter, 5 - Jester, 6 - Sheriff, 7 - Medic, 8 - Survivor, 9 - Guardian Angel, 10 - Altruist, 11 - Guesser Wolf
# Town: Villager, Naughty Girl, Drunk, Hunter, Sheriff, Medic
# Neutral: Jester, Survivor, Guardian Angel
# Evil: Werewolf
rolenames = ["Villager", "Werewolf", "Naughty Girl", "Drunk", "Hunter", "Jester", "Sheriff", "Medic", "Survivor", "Guardian Angel", "Altruist", "Guesser Wolf"]
townrolelist = [0, 2, 3, 4, 6, 7, 10]
neutralrolelist = [5, 8, 9]
evilrolelist = [1, 11]

playerlist = []
playernamelist = []
roleslist = []
devmode = False

def displaynames():
    print(f"All {len(playernamelist)} players:")
    for name in playernamelist:
        print(name)
    print() # Leaves whitespace after names are displayed

def displayroles():
    print(f"All {len(rolenames)} roles:")
    for role in rolenames:
        print(role)
    print()  # Leaves whitespace after roles are displayed

while True:
    newplayername = input("Input player name: (Input '0' once all players are in or '-1' to reset all names)\n")
    if newplayername == '0':
        if len(playernamelist) >= 3:
            displaynames()
            allplayernamesconfirm = intinputvalidate("Is this all players? (1=Yes, 0=No, add more)\n", 0, 1)
            if allplayernamesconfirm:
                break
        else:
            print("You must have at least 3 players to play")
    elif newplayername == '-1':
        playernamelist = []
        roleslist = []
        print("All names reset, please input all player names again")
    else:
        if newplayername not in playernamelist:
            print(f"Name: {newplayername}")
            playernamelist.append(newplayername)
            roleslist.append(0)
            if newplayername == '`dev`':
                print("devmode activated")
                devmode = True
        else:
            print("Name is already taken")


# Roles setup

playernum = len(playernamelist)
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
        evilroleselect = randint(0, len(evilrolelist)-1)
        evilroleselect = 1
        roleslist[i] = evilrolelist[evilroleselect]


# Other roles

guardianangelid = None

otherroleslist = townrolelist + neutralrolelist
if playernum - werewolfnum > len(otherroleslist):
    for i in range(playernum - werewolfnum - len(otherroleslist)):
        otherroleslist.append(0)  # Adds a villager for each extra player

for i in range(len(roleslist)):
    if roleslist[i] in evilrolelist:
        continue
    else:
        roleslist[i] = otherroleslist.pop(randint(0, len(otherroleslist) - 1))
        if roleslist[i] == 9: # Guardian Angel
            guardianangelid = i


# Player Instantiation

for i in range(playernum):
    playerlist.append(Player(i, playernamelist[i], roleslist[i]))


# Guardian Angel Selection

if guardianangelid != None:
    while True:
        guardianangelprotectingid = randint(0, playernum-1)
        if guardianangelprotectingid != guardianangelid:
            break
    playerlist[guardianangelprotectingid].guardian = True
    for i in range(playernum): # Applies to all players in case the guardian angel role is swapped
        playerlist[i].guardianangelprotectingid = guardianangelprotectingid


print("\nAll roles have been allocated.")
sleep(3)
clearscreen()

night = 1


# Subroutines

def playerselectnotself(playerid):
    selectid = 0 # Placeholder in case of error

    while True:
        flag = False
        otherflag = False
        selectname = input("Input the name of the player you would like to select: (leave empty to display all player names)\n")
        if selectname == '':
            displaynames()
        else:
            for i in range(playernum):
                if playerlist[i].name == selectname:
                    if i == playerid:
                        print("You can't select yourself")
                        otherflag = True
                    else:
                        if not playerlist[i].living:
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


def playerselectforvote():
    selectid = 0 # Placeholder in case of error

    while True:
        flag = False
        otherflag = False
        selectname = input("Input the name of the player you would like to select: (press enter to display all player names, enter 'skip' to skip vote)\n")
        if selectname == '':
            displaynames()
        elif selectname == 'skip':
            return 'skip'
        else:
            for i in range(playernum):
                if playerlist[i].name == selectname:
                    if not playerlist[i].living:
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


def roleselect():
    selectid = 0 # Placeholder in case of error

    while True:
        flag = False
        selectrole = input("Input the role you would like to select: (leave empty to display all roles)\n")
        if selectrole == '':
            displayroles()
        else:
            for i in range(len(rolenames)):
                if rolenames[i] == selectrole:
                    selectid = i
                    flag = True
            if flag:
                break
            else:
                print("Role not found")
    return selectid


def checkwin():
    aliveplayersnum = 0
    alivewerewolvesnum = 0

    for i in range(playernum):
        if playerlist[i].living:
            aliveplayersnum += 1

    for i in range(playernum):
        if playerlist[i].roleid in evilrolelist:
            if playerlist[i].living:
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
    playername = playerlist[playerid].name
    print(f"Pass the device to player {playername}")
    sleep(1)

    input(f"Player {playername}, press enter when you are ready\n")

    print(f"\033[31mALL PLAYERS EXCEPT PLAYER {playername} LOOK AWAY\033[0m")
    if not devmode:
        print("3", end="\r")
        sleep(1)
        print("2", end="\r")
        sleep(1)
        print("1", end="\r")
        sleep(1)


# Character Actions

def disguiseact():
    print("You will be asked to input two players' names to disguise your role")
    for i in range(2):
        disguisecode = playerlist[randint(0, playernum-1)].name
        while True:
            cmd = input(f"Input the name '{disguisecode}'\n")
            if cmd == disguisecode:
                break
            else:
                print("Incorrect input")


def werewolfact(playerid):
    print("You must select a player to vote to kill them. One of the voted players will be killed at random")

    for i in range(len(werewolfkillvotes)):
        print(f"Werewolf {playerlist[werewolfkillvotes[i][1]]} voted to kill {playerlist[werewolfkillvotes[i][0]]} this night")

    killvote = playerselectnotself(playerid)
    werewolfkillvotes.append([killvote, playerid])

def werewolfkillconfirmed(deadplayer):
    print(f"Player {playerlist[deadplayer].name} has been killed by the werewolves.")
    playerlist[deadplayer].die()

def werewolfkill():
    deadplayer = werewolfkillvotes[randint(0, len(werewolfkillvotes)-1)][0]
    if not playerlist[deadplayer].protected:
        if altruistresult == None:
            werewolfkillconfirmed(deadplayer)
        else:
            print(f"The werewolves attempted to kill {playerlist[deadplayer].name}, but the altruist sacrificed themself")
            werewolfkillconfirmed(altruistresult)
    else:
        print(f"The werewolves attempted to kill {playerlist[deadplayer].name}, but they were protected")


def naughtygirlact(playerid):
    print("You will select two other players (not yourself) and swap their roles")
    select1 = playerselectnotself(playerid)
    while True:
        select2 = playerselectnotself(playerid)
        if select2 != select1:
            break
        else:
            print("You can't select the same player again")

    playerlist[select1].roleid, playerlist[select2].roleid = playerlist[select2].roleid, playerlist[select1].roleid


def drunkact(playerid):
    print("You will select another player and swap your own role with theirs")
    select = playerselectnotself(playerid)

    playerlist[playerid].roleid, playerlist[select].roleid = playerlist[select].roleid, playerlist[playerid].roleid


def hunterdeathact(playerid):
    print("The Hunter has died, and can now select a player to kill")
    select = playerselectnotself(playerid)
    print(f"You chose to kill player {playerlist[select].name}")
    playerlist[select].die()


def sheriffact(playerid):
    # Placeholder values for return with no action
    hit = False
    select = -1

    print("You can choose a player to kill, but if you select an innocent you will die instead: You can freely kill any neutral or evil roles")
    killconfirm = intinputvalidate("Would you like to try to kill someone tonight? (1=Yes, 0=No)\n", 0, 1)
    if killconfirm:
        select = playerselectnotself(playerid)
        if playerlist[select].roleid in evilrolelist or playerlist[select].roleid in neutralrolelist: # Hit
            hit = True
        else: # Miss
            select = playerid # Returns the sheriff as the dead player

    return killconfirm, hit, select


def medicact(playerid):
    print("You can choose a player this round (not yourself) to protect them from being killed this night (some killing roles may bypass your protection)")
    select = playerselectnotself(playerid)
    print(f"Player {playerlist[select].name} will be protected this round")
    playerlist[select].protected = True


def survivoract(playerid):
    print("You are a neutral, and only win if you are alive when the game ends, whether the werewolves or villagers win")
    sleep(1)
    if playerlist[playerid].survivorprotectavailable:
        print("You can protect yourself from death for one night this game")
        protectconfirm = intinputvalidate("Would you like to protect yourself tonight? (1=Yes, 0=No)\n", 0, 1)
        if protectconfirm:
            playerlist[playerid].protected = True
            playerlist[playerid].survivorprotectavailable = False
    else:
        print("You have already used your one time protection this game, and can no longer act during the night. Try not to die")
        disguiseact()


def guardianangelact(playerid):
    protectingplayerid = playerlist[playerid].guardianangelprotectingid
    print(f"You are protecting Player {playerlist[protectingplayerid].name}, who is a {rolenames[playerlist[protectingplayerid].roleid]}. You can only win if this player wins.")
    print("They know they have a guardian angel, but don't know who you are. If they die, you will become a Survivor")
    print()
    if playerlist[playerid].guardianangelprotectavailable:
        print("You can protect this player from death for one night this game")
        protectconfirm = intinputvalidate("Would you like to protect them tonight? (1=Yes, 0=No)\n", 0, 1)
        if protectconfirm:
            playerlist[protectingplayerid].protected = True
            playerlist[playerid].guardianangelprotectavailable = False
    else:
        print("You have already used your one time protection this game, and can no longer act during the night. Hope they don't die")
        disguiseact()


def altruistact(playerid):
    print("You can choose to redirect tonight's werewolf kill to kill you instead")
    altruistconfirm = intinputvalidate("Would you like to sacrifice yourself tonight? (1=Yes, 0=No)\n", 0, 1)
    if altruistconfirm:
        print("You will be remembered.")
        return playerid
    else:
        return None


def vote(playerid):
    if playerlist[playerid].roleid not in evilrolelist and playerlist[playerid].roleid != 5:
        print("You can select a player to vote who you think is a werewolf, or you can skip vote. Remember, if a jester is voted out then they will win")
    elif playerlist[playerid].roleid in evilrolelist:
        print("You can vote someone out of the game, votes are private so don't vote for another werewolf, or you can skip vote. Remember, if a jester is voted out then they will win")
    else:
        print("You are the jester, so if you get voted out you will win. Voting yourself is likely the best option here, however you are allowed to vote for anyone or skip vote")
    sleep(1)

    votedplayer = playerselectforvote()
    return votedplayer


def snipe(playerid):
    # Return: Snipe attempt true/false, snipe succeed true/false, id of sniped player on hit/sniper on miss

    print("You are a werewolf, so if you believe you know another player's role, you can guess it to kill them instantly. However, if you are incorrect then you will die instead")
    sleep(1)

    if playerlist[playerid].roleid == 11:
        if playerlist[playerid].doubleshotavailable:
            print("Because you are the Guesser Wolf, you are protected for one incorrect guess this game")
        else:
            print("You are the Guesser Wolf, but you have already used your one incorrect guess this game")
        sleep(1)

    snipeconfirm = intinputvalidate("Would you like to guess another player's role? (1=Yes, 0=No)\n", 0, 1)
    if snipeconfirm:
        snipedplayerid = playerselectnotself(playerid)
        snipedplayerrole = roleselect()
        if playerlist[snipedplayerid].roleid == snipedplayerrole:
            return True, True, snipedplayerid
        else:
            return True, False, playerid
    else:
        return False, False, -1


# Game Loop

night = 0
jesterwin = False
run = True
while run:
    night += 1 # Increments night counter at the start of the game loop, starting at 1

    werewolfkillvotes = [] # Resets werewolf kill votes at the start of the game loop
    sheriffresult = [False, False, -1] # Resets sheriff result at the start of the game loop
    altruistresult = None # Resets altruist result at the start of the game loop

    for i in range(playernum):
        if playerlist[i].roleid == 9:
            if not playerlist[playerlist[i].guardianangelprotectingid].living:
                playerlist[i].roleid = 8

    roleslistnightcopy = [] # List of player roles that won't change if roles are swapped during the night
    for i in range(playernum):
        roleslistnightcopy.append(playerlist[i].roleid)
        playerlist[i].protected = False # Resets protection list at the start of the game loop


    # Werewolf ally list updates at start of night
    werewolfallylist = []
    for j in range(len(roleslist)):
        if roleslist[j] == 1:
            werewolfallylist.append(playerlist[j])

    for i in range(playernum):
        playername = playerlist[i].name # For easy use in the for loop

        # Night number stays at top for the whole night
        clearscreen()
        print(f"Night {night}\n")
        sleep(1)

        if playerlist[i].living:
            privateplayerchoiceprep(i)

            if playerlist[i].roleid == 0 or playerlist[i].roleid in evilrolelist: # Can be multiple villagers/werewolves
                print(f"Player {playername}, you are a {rolenames[roleslistnightcopy[i]]}")
            else: # Only one of each other role
                print(f"Player {playername}, you are the {rolenames[roleslistnightcopy[i]]}")
            sleep(1)

            if playerlist[i].guardian:
                print("You have a Guardian Angel who is trying to help you win. They know you and your role but you don't know who they are")
                sleep(1)

            match roleslistnightcopy[i]:
                case 0: # Villager
                    disguiseact()
                case 1: # Werewolf
                    # Displays all werewolf allies
                    if len(werewolfallylist) > 1:
                        print("The werewolves are:")
                        for ally in werewolfallylist:
                            print(ally)

                    werewolfact(i)
                case 2: # Naughty Girl
                    naughtygirlact(i)
                case 3: # Drunk
                    drunkact(i)
                case 4: # Hunter
                    print("When you die, you will be able to kill a player of your choice. Try to kill a werewolf")
                    disguiseact()
                case 5: # Jester
                    print("Your goal is to be voted out by the other players. If this happens you will win, but if you are killed then you lose")
                    disguiseact()
                case 6: # Sheriff
                    sheriffresult = sheriffact(i)
                case 7: # Medic
                    medicact(i)
                case 8: # Survivor
                    survivoract(i)
                case 9: # Guardian Angel
                    guardianangelact(i)
                case 10: # Altruist
                    altruistresult = altruistact(i)
                case 11: # Guesser Wolf
                    if playerlist[i].doubleshotavailable:
                        print("You are a werewolf ally who gets a second life when guessing roles")
                    else:
                        print("You have used up your guessing second life. Be cautious when guessing again")

                    # Displays all werewolf allies
                    if len(werewolfallylist) > 1:
                        print("The werewolves are:")
                        for ally in werewolfallylist:
                            print(ally)

                    werewolfact(i)
                case _:
                    print("Role not found")

        else:
            print(f"Player {playername} is dead.")

        input("Press enter when you are ready to end your action and move on to the next player:\n")

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
        if sheriffresult[1]: # If the sheriff correctly killed non-town
            if playerlist[sheriffresult[2]].protected:
                print(f"The sheriff attempted to kill player {playerlist[sheriffresult[2]].name}, but they were protected")
            else:
                print(f"The sheriff correctly killed player {playerlist[sheriffresult[2]].name}")
        else: # The sheriff incorrectly shot and killed themselves
            print(f"The sheriff {playerlist[sheriffresult[2]].name} attempted to shoot an innocent and instead killed themself")
        playerlist[sheriffresult[2]].die()
        sleep(1)

    checkwinresult = checkwin()
    if checkwinresult[0]: # If there has been a win, exit the game loop
        run = False
    else: # Otherwise, the players will vote someone out
        print("It is time to vote a player out. Discuss amongst yourselves who you want to vote")
        sleep(1)
        input("Press enter when everyone is ready to vote\n")

        votelist = []
        sniperesultlist = []
        for i in range(playernum):
            clearscreen()
            print(f"Day {night}\n")  # Night counter = Day counter
            sleep(1)

            if playerlist[i].living:
                privateplayerchoiceprep(i)

                if playerlist[i].roleid in evilrolelist:
                    sniperesultlist.append(snipe(i))
                    print()
                    sleep(1)

                playervote = vote(i)

                voteflag = True
                for j in range(len(votelist)):
                    if votelist[j][0] == playervote:
                        votelist[j][1] += 1
                        voteflag = False
                if voteflag: # If vote not already in list
                    votelist.append([playervote, 1])

            else:
                print(f"Player {playerlist[i].name} is dead")
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
            if votedplayer != 'skip':
                print(f"Player {playerlist[votedplayer].name} was voted out.")
                playerlist[votedplayer].die()
                if roleslist[votedplayer] == 5:
                    jesterwin = True
                    run = False
            else:
                print("The players chose to skip the vote")
        else: # In case of a tie
            print(f"There was a tie in votes between {len(votedplayerlist)} players:")
            for playerid in votedplayerlist:
                print(playerlist[playerid].name)
            print("Because there was a tie in votes, no one will be removed from the game")

        if len(sniperesultlist) > 0:
            if sniperesultlist[i][0]:
                if sniperesultlist[i][1]:
                    print(f"A werewolf correctly guessed the role of player {playerlist[sniperesultlist[i][2]].name}")
                    playerlist[sniperesultlist[i][2]].die()
                else:
                    if playerlist[sniperesultlist[i][2]].roleid == 11 and playerlist[sniperesultlist[i][2]].doubleshotavailable: # If role is Guesser Wolf and they have their double shot available
                        playerlist[sniperesultlist[i][2]].doubleshotavailable = False # Double shot is used up
                    else:
                        print(f"Player {playerlist[sniperesultlist[i][2]].name} attempted to guess another player's role but was incorrect")
                        playerlist[sniperesultlist[i][2]].die()

        checkwinresult = checkwin()
        if checkwinresult[0]:
            run = False
        else:
            sleep(1)
            input("\nPress enter when everyone is ready for the next night:\n")


# Main winners

if not jesterwin:
    if checkwinresult[1] == 1:
        print("The villagers have won!")
    elif checkwinresult[1] == 2:
        print("The werewolves have won!")
else:
    print("The jester has won!")

sleep(1)

# Other winners

# Survivor win
for i in range(playernum):
    if roleslist[i] == 8:
        if playerlist[i].living:
            print(f"Player {playerlist[i].name} also won, as they were the survivor and lived to the end of the game!")

sleep(10)
