class Actor(object):
    def __init__(self, name, level, attack, defence, health):
        self.name = name
        self.level = level
        self.attack = attack
        self.defence = defence
        self.health = health
        self.maxHP = health
    def __str__(self):
        return """%s:
Lvl: %i    HP: %i
Atk: %i    Def: %i
""" % (self.name, self.level, self.health, self.attack, self.defence)
    def IsAlive(char):
        if char.health > 0:
            return True
        else:
            return False

class Null(Actor):
    def __init__(self):
        self.level = 0
    def IsAlive(self):
        return False
NoMon = Null()

class Monster(Actor):
    def __init__(self, name, level):
        Actor.__init__(self, name, level, level+1, level+1, level*5)
    def __str__(self):
        return """%s:
Lvl: %i    HP: %i""" % (self.name, self.level, self.health)

class Player(Actor):
    def __init__(self, name, level):
        Actor.__init__(self, name, level, level+1, level+1, level*5+5)
        self.magic = level+1
        self.maxMP = level+1
        self.exp = 0
        self.spells = [Flare, Stars, Thunder]
    def __str__(self):
        return """
%s:
Lvl: %i    XP: %i
HP: %i/%i  MP: %i/%i
Atk: %i    Def: %i
""" % (self.name, self.level, self.exp, self.health, self.maxHP, self.magic, self.maxMP, self.attack, self.defence)

class Tile(object):
    def __init__(self, name, look, special=None):
        self.name = name
        self.look = look
        self.special = special
    def __str__(self):
        return "%s: %s" % (self.name, self.look)

class Camp(Tile):
    def __init__(self, name, look, monster1, monster2=NoMon):
        Tile.__init__(self, name, look, None)
        self.monster1 = monster1
        self.monster2 = monster2

class Boss(Tile):
    def __init__(self, name, look, monster1, monster2=NoMon, loot=None):
        Tile.__init__(self, name, look, "Boss")
        self.monster1 = monster1
        self.monster2 = monster2
        self.loot = loot

class Spell(object):
    def __init__(self, name, message, cost=1, bonus=2, special=""):
        self.name = name
        self.message = message
        self.cost = cost
        self.bonus = bonus
        self.special = special
    def __str__(self):
        if self.special == "":
            return "%s: %i MP" %(self.name, self.cost)
        else:
            return "%s: %i MP -- %s" %(self.name, self.cost, self.special)

Flare = Spell("Flare","You launch a blast of fire at",1,2,"")
Thunder = Spell("Thunder","You launch a lightning bolt at",2,5,"")
Stars = Spell("Stars","You launch a cone of stars at",2,0,"Split")
Ice = Spell("Ice","You launch two ice spikes at",3,0,"Double")

from random import randint
from time import sleep
from threading import Thread
import sys

def roll():
    rollnum = float(randint(3,7))/2
    if rollnum >= 3.0:
        rollnum = float(randint(3,7))/2
    return rollnum

fail = False
answer = None

def check():
    global fail
    global answer
    answer = None
    sleep(0.5)
    if answer != None:
        fail=False
        return
    else:
        print("X")
        sys.stdout.flush()
        fail=True
        return

def Action():
    global answer
    delay=randint(4,12)
    for i in range(0,delay):
        print("-",end="")
        sys.stdout.flush()
        sleep(0.5)
    Thread(target = check).start()
    answer = input(">")
    if fail == True:
        return 0
    else:
        return 1

def Fight(attacker,target,bonus=0,action=True):
    damage=attacker.attack
    damage+=bonus
    damage*=roll()
    act=0
    if attacker==Player and action==True:
        act=Action()
    if act==1:
        print("Perfect hit! ",end="")
        damage+=randint(1,2)
    damage-=target.defence
    damage=int(damage)
    if damage<0:
        damage=0
    target.health-=damage
    print("%s takes %i damage from %s!" %(target.name,damage,attacker.name))
    if target.IsAlive() == False:
        print("%s dies!" %(target.name))

def Run_Away():
    print("You attempt to flee the battle.\n")
    if randint(1,3) == 1:
        print("You can't get away!\n")
        return False
    else:
        print("You escape the battle.\n")
        return True

def BatTarget(foe1, foe2):
    if foe1.IsAlive() and foe2.IsAlive() == True:
        while 1==1:
            print("Who do you want to target?")
            target=input("[1] %s or [2] %s?\n>" %(foe1.name, foe2.name))
            if target=="1":
                return foe1
            elif target=="2":
                return foe2
            else:
                print("Not sure what you mean.")
    elif foe2.IsAlive() == True:
        return foe2
    else:
        return foe1

def BatFoeTurn(foe1, foe2):
    if foe1.IsAlive() and foe2.IsAlive():
        Fight(foe1,Player,randint(-1,0))
        Fight(foe2,Player,randint(-1,0))
    if foe1.IsAlive() and (not foe2.IsAlive()):
        Fight(foe1,Player)
    if foe2.IsAlive() and (not foe1.IsAlive()):
        Fight(foe2,Player)
    if foe1.IsAlive() or foe2.IsAlive():
        return True
    else:
        return False

def Battle(foe1,foe2=NoMon):
    foe1.health=foe1.maxHP
    if type(foe2)!=Null:
        foe2.health=foe2.maxHP
    while Player.IsAlive()==True:
        print(Player)
        if foe1.IsAlive() == True:
            print(foe1)
        if type(foe2)!=str:
            if foe2.IsAlive() == True:
                print(foe2)
        cmd = input("\n[A]ttack, [M]agic or [F]lee?\n>")
        if cmd == "A" or cmd == "a":
            target = BatTarget(foe1,foe2)
            Fight(Player,target)
            check = BatFoeTurn(foe1,foe2)
            if check == False:
                break
        elif cmd == "M" or cmd == "m":
            check=CastSpell(foe1,foe2)
            if check == "FoeTurn":
                check2 = BatFoeTurn(foe1,foe2)
                if check2 == False:
                    break
        elif cmd == "F" or cmd == "f":
            check=Run_Away()
            if check == True:
                break
            check = BatFoeTurn(foe1,foe2)
            if check == False:
                break
        else:
            print("Not sure what you want.")
    if foe1.IsAlive or foe2.IsAlive == False:
        Player.exp+=foe1.level
        Player.exp+=foe2.level
        if Player.exp >= Player.level*5:
            LevelUp()
        return "Clear"
    return ""

def CastSpell(target1,target2):
    for magic in Player.spells:
        print("[%s]: %s" %(Player.spells.index(magic)+1,magic))
    choice=int(input("Which spell do you want?\n>"))
    choice-=1
    try:
        cast=Player.spells[choice]
    except IndexError:
        print("You don't have that many spells.")
        return ""
    if cast.cost>Player.magic:
        print("You don't have enough MP.")
        return ""
    if cast.special=="Split":
        Player.magic-=cast.cost
        print(cast.message+" %s and %s!"%(target1.name,target2.name))
        Fight(Player,target1,cast.bonus)
        Fight(Player,target2,cast.bonus,False)
        return "FoeTurn"
    elif cast.special=="Double":
        target = BatTarget(target1,target2)
        Player.magic-=cast.cost
        print(cast.message+" %s!"%(target1.name))
        Fight(Player,target,cast.bonus)
        Fight(Player,target,cast.bonus,False)
        return "FoeTurn"
    else:
        target = BatTarget(target1,target2)
        Player.magic-=cast.cost
        print(cast.message+" %s!"%(target.name))
        Fight(Player,target,cast.bonus)
        return "FoeTurn"

def Town(townname):
    while 1==1:
        print(Player)
        print("You are in %s.\nWhat do you want to do?"%(townname))
        cmd = input("[R]est at an inn, leave to [E]xplore or retire and [Q]uit?\n>")
        if cmd == "R" or cmd == "r":
            Player.health = Player.maxHP
            Player.magic = Player.maxMP
            print("\nA good rest heals the body and mind.")
        elif cmd == "E" or cmd == "e":
            break
        elif cmd == "Q" or cmd == "q":
            global Retire
            Retire=True
            break
        else:
            print("Not sure what you want.")

def Explore(Y,X):
    Location = Map[Y][X]
    while 1==1:
        if EncounterMap[Y][X] == 1:
            ambush = randint(1,6)
            if ambush == 1:
                print("You are ambushed by a %s!"%(Location.monster1.name))
                check=Battle(Location.monster1,Location.monster2)
                if check=="Clear":
                    EncounterMap[Y][X]-=1
                return [0,0]
        print(Player)
        print(Location)
        east=Map[Y][X+1]
        west=Map[Y][X-1]
        south=Map[Y+1][X]
        north=Map[Y-1][X]
        print('[N]orth: %s\n[S]outh: %s\n[E]ast: %s\n[W]est: %s' %(north.name,south.name,east.name,west.name))
        if Location.special == "Town":
            print("The [T]own of %s is here."%(Location.name))
        if EncounterMap[Y][X] == 1:
            print("There is a %s here to [A]ttack."%(Location.monster1.name))
        cmd = input("What do you want to do?\n>")
        if cmd == "N" or cmd == "n":
            if north.special != "Block":
                return [-1,0]
            else:
                print("You can't go that way.")
        elif cmd == "S" or cmd == "s":
            if south.special != "Block":
                return [+1,0]
            else:
                print("You can't go that way.")
        elif cmd == "E" or cmd == "e":
            if east.special != "Block":
                return [0,+1]
            else:
                print("You can't go that way.")
        elif cmd == "W" or cmd == "w":
            if west.special != "Block":
                return [0,-1]
            else:
                print("You can't go that way.")
        elif cmd == "T" or cmd == "t":
            if Location.special == "Town":
                Town(Location.name)
                return [0,0]
            else:
                print("There is no town here.")
        elif cmd == "A" or cmd == "a":
            if EncounterMap[Y][X] == 1:
                check=Battle(Location.monster1,Location.monster2)
                if check=="Clear":
                    EncounterMap[Y][X]-=1
                return [0,0]
            else:
                print("There's nothing to attack here.")
        else:
            print("Not sure what you want.\n")

def LevelUp():
    Player.exp-=Player.level*5
    Player.level+=1
    Player.attack+=1
    Player.defence+=1
    Player.maxHP+=5
    Player.maxMP+=1
    if Ice not in Player.spells:
        Player.spells.append(Ice)
    print("You level up! You are now Level %i!" %Player.level)

#PlayerName = input("What is your name? ")
PlayerName = "Nick"
Player = Player(PlayerName, 1)
Goblin = Monster("Goblin",1)
Wolf = Monster("Wolf",1)
Orc = Monster("Orc",2)
Troll = Monster("Troll",3)
Dragon = Monster("Dragon",5)
Dragon.maxHP+=10
M0 = Tile("Mountain","","Block")
M1 = Tile("Mountain","","Block")
M2 = Tile("Mountain Pass","Passage beyond the mountains","")
T1 = Tile("Northpoint","A large town","Town")
T2 = Tile("Erinstead","A small village","Town")
F1 = Camp("Plain","A flat plain",Goblin)
F0 = Camp("Forest","A calm forest",Goblin,Wolf)
F2 = Camp("Forest","A calm forest",Orc)
F3 = Camp("Hills","Rolling hills",Troll)
F4 = Camp("Hills","Rolling hills",Orc,Goblin)
C1 = Boss("Castle","A large castle",Dragon)
Map = [
[M0, M0, M0, M0, M0, M0, M0, M0, M0, M0],
[M0, T1, F1, F1, F1, F2, F2, F0, F2, M0],
[M0, F1, F1, F1, F1, F2, F2, F2, F0, M0],
[M0, F1, F1, F1, F1, F1, F2, F2, F2, M0],
[M0, F1, F1, F1, F1, F1, F1, F0, F2, M0],
[M0, M1, M1, M2, M1, M1, M2, M1, M1, M0],
[M0, F2, F2, F2, F2, F0, F0, F2, F4, M0],
[M0, F2, F0, T2, F0, F2, F3, F4, F3, M0],
[M0, F2, F2, F2, F0, F2, F3, C1, F3, M0],
[M0, F0, F2, F0, F2, F3, F4, F3, F3, M0],
[M0, M0, M0, M0, M0, M0, M0, M0, M0, M0]]
EncounterMap = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 1, 2, 2, 1, 1, 1, 0],
[0, 1, 1, 2, 2, 2, 2, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
CoorX=1
CoorY=1
Retire=False
Battle(Goblin,Wolf)
while Player.IsAlive()==True:
    Move=[0,0]
    Move=Explore(CoorY,CoorX)
    CoorX+=Move[1]
    CoorY+=Move[0]
    if Retire==True:
        break
print("Game ended.")
if Player.IsAlive()==False:
    print("You died at level %i." %(Player.level))
else:
    print("You retired at level %i." %(Player.level))
