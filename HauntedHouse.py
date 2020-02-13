import random
import sys
from termcolor import colored, cprint

def printBold(text):
    print(colored(text,attrs=['bold']))
    
def printUnder(text):
    print(colored(text,attrs=['underline']))

class Entity():
#instances of this class are created with a number of hit points (HP)
    #determines how healthy is the entity
#and a value of armor class (AC)
    #determines how hard it is to hit the entity
    def __init__(self, name, maxHP, AC):
        self.name = name
        self.maxHP = maxHP
        self.HP = maxHP
        self.AC = AC
        self.alive = True
        self.has_usables = 0
        self.stunned = 0
        
    def __str__(self):
        return ('This ' + self.name + ' has ' + str(self.HP) + ' HP and '+ str(self.AC) + ' AC.') 
    
    def rolls_initiative(self):
        initiative = random.randint(1,21)
        print (self.name + ' rolls for initiative: ' + str(initiative)) 
        return initiative 
        
    def is_attacked(self,incoming_hit,incoming_damage):
        if incoming_hit >= self.AC:
            self.HP -= incoming_damage
            print ('You hit.',self.name + ' takes ' + str(incoming_damage) + ' damage.')
            if self.HP <= 0:
                printBold (self.name + ' is dead.')
                self.alive = False
        else:
            print (self.name + ' avoids the attack.')
    
    def is_stunned(self):
        print (self.name + ' is STUNNED! Doesn`t attack this turn.')
        self.stunned = 1
        
    def is_immobilized(self):
        print (self.name + ' is IMMOBILIZED. Can`t chase its opponent.')
        
    def rests(self):
        shortrest = random.randint(6,13)
        self.HP += shortrest
        if self.HP > self.maxHP:
            self.HP = self.maxHP
        print (self.name + ' has rested. Currently has ' + str(self.HP) + ' out of ' + str(self.maxHP) + ' hit points.') 
    
class Player(Entity):
   
    def checks_inventory(self):
        backpack.contains()
        if number_of_keys >= 4:
            print('\n *** Well done, you have four keys! Now you can open the vault doors. *** ')
    def loots(self, container_to_loot):
        if len(container_to_loot) != 0: 
            for item in container_to_loot:
                backpack.add(item)
            print (' -> Stuff moved to your backpack.')
            
    def chooses_weapon(self):
        weapon_arsenal = {'Fists':4, 
                          'Axe':8, 
                          'Shotgun':14}
        print('\nYou have the following weapons at your disposal:')
        for key in weapon_arsenal.keys():
            print(key)
        weapon_type = input('Which to use?').lower()
        if weapon_type.startswith('f'): weapon_type = 'Fists'
        elif weapon_type.startswith('a'): weapon_type = 'Axe'
        elif weapon_type.startswith('s'): weapon_type = 'Shotgun'
        else:
            print('You don`t have that. Using your fists for now.')
            weapon_type = 'Fists'
        max_weapon_damage = weapon_arsenal[weapon_type]
        return max_weapon_damage

    def is_attacked(self,attacker_name,incoming_hit,incoming_damage):
        if incoming_hit >= self.AC:
            self.HP -= incoming_damage
            print('\nYou are hit and take ' + str(incoming_damage) + ' damage.')
            print(self.name + ', you have ' + str(self.HP) + ' HP left.')
            if self.HP <= 0:
                print (self.name + ', you are dead.')
                self.alive = False
        else:
            print (attacker_name + ' attacks but you avoid the strike.')
    def rolls_initiative(self):
        initiative = random.randint(1,21)
        print ('\n' + self.name + ' rolls for initiative: ' + str(initiative)) 
        return initiative 
    def checks_usables(self):
        #compares backpack contents against a list of usable items
        #modifies has_usables class attribute
        usables = ['Bandage','Flashbang']
        if usables[0] in backpack.contents or usables[1] in backpack.contents:
            self.has_usables = 1
            print ('\nYou can use:')
            for i in usables:
                if i in backpack.contents:
                    print (i)
        else:
            print('\nWhoopsie, you are all out of usable items.')
            self.has_usables = 0
    
    def uses_item(self):
        item_to_use = ''
        while item_to_use == '':
            item_to_use = input('Select item to use or close backpack').lower()
        if item_to_use.startswith('b') and 'Bandage' in backpack.contents:
            self.HP += random.randint(6,12)
            if self.HP > self.maxHP:
                self.HP = self.maxHP
            print ('You are healed to ' + str(self.HP) + ' HP.')
            backpack.remove('Bandage')
        elif item_to_use.startswith('f') and 'Flashbang' in backpack.contents:
            if fighting:
                monster.is_stunned()
            else:
                print(' *** The flashbang discharges in your hand leaving you momentarily dazed. Well played. *** ')
            backpack.remove('Flashbang')
        elif item_to_use.startswith('c'):
            pass
        else: 
            print('Not usable.')
    
class Container():
#blueprint for a container
    def __init__(self,name):
        self.name = name
        self.contents = []
        
    def contains(self):
        if self.contents != []:
            printUnder(self.name + ' contains:')
            for item in self.contents:
                if 'key' in item:
                    print(colored(item, 'yellow'))
                elif 'Bandage' in item:
                    print(colored(item, 'blue'))
                elif 'Flashbang' in item:
                    print(colored(item, 'red'))
                else:
                    print(item)
        else:
            print(self.name,'is empty.')
        
    def add(self, item_in):
        self.contents.append(item_in)
    def remove(self,item_out):
        self.contents.remove(item_out)
    def is_looted(self):
        self.contents.clear()
    def is_trapped(self):
        if random.randrange(1,100) < 60:
            print('The '+ self.name + ' is trapped!')
            traps = {'Dart trap':4, 'Poison gas':8, 'Explosion':12}
            #is_attacked(self,attacker_name,incoming_hit,incoming_damage)
            #incoming_hit is randrange
            #incoming_dmg is tied to randomly chosen element from dict traps
            player.is_attacked(random.choice(list(traps.keys())),
                               random.randrange(10,15), traps[random.choice(list(traps.keys()))])
    def hides_key(self):
        if random.randrange(1,100) < 30:
            key_types = ['Brass key', 'Gold key', 'Silver key', 'Copper key']
            type_of_key = random.choice(key_types)
            self.contents.append(type_of_key)
            global number_of_keys
            number_of_keys+=1
class Location():
#instances of this class are created with a name of the room
#and an indicator of danger
    #0 for no enemy - this is default, 1 for enemy present
    def __init__(self,name,danger=0):
        self.name = name
        self.danger = danger
        
    def __str__(self):
        return self.name
        
    def has_enemy(self):    
        creatures = ['Groggy ghost','Blob of goo','Ghoul','Poltergeist',
                     'Ghastly pirate','Sad vampire','Lidless eye','Moaning monster',
                     'Chucking woodchuck','Batswarm','Striga','Besny havko',
                     'Creepy doll','Axe murderer','Norman Bates'
                    ]
        monster = Entity(random.choice(creatures),18,10)
        print('\nAfter entering the '+self.name +', you are attacked by a '+ monster.name +'.')
        fighting = 1
        max_weapon_damage = player.chooses_weapon()
        return monster,fighting,max_weapon_damage
    
    def whatInRoom(self,itemDic):   
#deals with player choice, keys, trapped containers and looting 
#before calling this function, need to fill given containers, place keys
#argument is a disctionary of containers and their items - up to 4 containers and no limit on number of items
#'CONTAINER':'ITEM1','ITEM2','ITEM3',...
    
        global in_house
        global end_it 
        in_room = 1
        containers = []
        conts_abb = []
        for key in itemDic.keys(): containers.append(key), conts_abb.append(key[0].lower())
        conts_abb += ['b','r','e']
        try:
            cont0 = Container(containers[0])
            cont0.hides_key()
            for item in itemDic[containers[0]]:
                cont0.add(item)
        except IndexError: pass
        try:
            cont1 = Container(containers[1])
            cont1.hides_key()
            for item in itemDic[containers[1]]:
                cont1.add(item)
        except IndexError: pass
        try:
            cont2 = Container(containers[2])
            cont2.hides_key()
            for item in itemDic[containers[2]]:
                cont2.add(item)
        except IndexError: pass
        try:
            cont3 = Container(containers[3])
            cont3.hides_key()
            for item in itemDic[containers[3]]:
                cont3.add(item)
        except IndexError: pass    

        while in_room:
            if len(containers) !=0:
                print('\nIn this room you can explore:')
                for key in itemDic.keys(): print(key)
                print('Alternatively, you can check your backpack, push on to another room or escape screaming.')

            else:
                print('This rooms seems empty. Want to rummage through your backpack or contuinue exploring?')
            room_choice = input().lower()
            while room_choice == '' or room_choice[0] not in conts_abb:
                room_choice = input('The room gives you chills. What do you do?').lower()
            try:    
                if room_choice[0] == containers[0][0].lower():
                    cont0.is_trapped()
                    if not player.alive: 
                        in_room, in_house, end_it = 0,0,1
                        break 
                    cont0.contains()
                    player.loots(cont0.contents)
                    cont0.is_looted() 
            except IndexError: pass
            try:
                if room_choice[0] == containers[1][0].lower():
                    cont1.is_trapped()
                    if not player.alive: 
                        in_room, in_house, end_it = 0,0,1
                        break
                    cont1.contains()
                    player.loots(cont1.contents)
                    cont1.is_looted() 
            except IndexError: pass
            try:
                if room_choice[0] == containers[2][0].lower():
                    cont2.is_trapped()
                    if not player.alive: 
                        in_room, in_house, end_it = 0,0,1
                        break
                    cont2.contains()
                    player.loots(cont2.contents)
                    cont2.is_looted()
            except IndexError: pass
            try:
                if room_choice[0] == containers[3][0].lower():
                    cont3.is_trapped()
                    if not player.alive: 
                        in_room, in_house, end_it = 0,0,1
                        break
                    cont3.contains()
                    player.loots(cont3.contents)
                    cont3.is_looted()
            except IndexError: pass
            if room_choice[0] == 'b':
                player.checks_inventory()
                player.checks_usables()
                if player.has_usables:
                    player.uses_item()
            if room_choice[0] == 'r':
                room_exit_lines = ['\n *** You push open the door and face another room. *** ', 
                              '\n *** You leave the room and journey deeper into the house. *** ',
                              '\n *** Full of hopes, you carry on. *** ',
                              '\n *** You continue exploring. *** ',
                              '\n *** Your footsteps echo in the quiet interior.*** ']     
                room_exit_line = random.choice(room_exit_lines)
                print(room_exit_line)
                in_room = 0
            if room_choice == 'e':
                in_room, in_house, end_it = 0,0,1
                print(' *** Smart. You leave the house. *** ')
        

def combat(player,monster,fighting,max_weapon_damage):
    
        if int(player.rolls_initiative()) > int(monster.rolls_initiative()):
            print ('\nYou react faster.')
            ###if player wins initiative, let him choose to fight or check inventory and use item
            if input('\nFight or use item?').lower().startswith('f'):
                monster.is_attacked(11,random.randint(1,max_weapon_damage))
                if not monster.alive:
                    fighting = 0
            else:
                player.checks_usables()
                if player.has_usables:
                    player.uses_item()
                if monster.stunned:
                    monster.is_attacked(11,random.randint(1,max_weapon_damage))
                    if not monster.alive:
                        fighting = 0
                else:
                    player.is_attacked(monster.name,random.randint(5,15),random.randint(2,10))
                    if not player.alive:
                        fighting = 0
        else:
            print ('\n' + monster.name + ' attacks first.')
            player.is_attacked(monster.name,random.randint(5,15),random.randint(2,10))
            if not player.alive:
                fighting = 0
            monster.is_attacked(11,random.randint(1,max_weapon_damage))
            if not monster.alive:
                fighting = 0
        return player,monster,fighting
            
printBold('Barry the Butler says: "Welcome to the haunted house."')
printBold('Barry the Butler says: "How would you like to be addressed?."')
player_name = input()
player = Player(player_name, 50, 12)
backpack = Container('Backpack')
printBold('Barry the Butler says: "' + player.name + ', the house holds many treasures."')
printBold('Barry the Butler says: "If you`re looking for the vault, be warned - you need to collect 4 keys."')
printBold('Barry the Butler says: "Enjoy your stay."')
number_of_keys = 0
in_house = 1
end_it = 0
while in_house:
    room1 = Location('Foyer')
    print('\n *** You enter the', room1.name +'. *** ')
    room1.whatInRoom({'Painting of lady and lord Durst':['Bleached letter'],
                'Wardrobe':['Bandage','Dusty duster']
               })
    if end_it: break
    room2 = Location('Grand hall')
    print('\n *** You find yourself in the ' + room2.name + '. *** ')
    monster, fighting,max_weapon_damage = room2.has_enemy() 
    while fighting:
        player,monster,fighting = combat(player,monster,fighting,max_weapon_damage)
    if not player.alive:
        in_house = 0
        break
    room2.whatInRoom({'Weapon cabinet':['Flashbang','Rusty nail'],
                'Iron lockbox':['Bag of coins','Polished emerald'],
                'Antique vase':['Dried tulips','Wasp nest']
               })
    if end_it: break
    room3 = Location('Kitchen')
    print('\n *** You enter the ' + room3.name + ' and smell stew cooking. *** ')
    monster,fighting,max_weapon_damage = room3.has_enemy() 
    while fighting:
        player,monster,fighting = combat(player,monster,fighting,max_weapon_damage)
    if not player.alive:
        in_house = 0
        break  
    room3.whatInRoom({'Shabby cupboard':['Bandage','Worm-ridden bag of flour'],
                'Wooden box':['Sack of turnips','Bunch of carrots'],
                'Kitchen counter':['Severed head of lady Durst']
               }) 
    if end_it: break
    room4 = Location('Long hallway')
    print(' *** Walking along a carpeted hallway you notice a secret compartment behind a rotten wallpaper. *** ')
    room4.whatInRoom({'Painting of a landscape':['"Merry marshes" by Catherine Durst: oil on canvas'],
                'Secret stash':['Huge ruby','Bloody ringfinger'],
                'First aid lockbox':['Bandage']
               }) 
    if end_it: break
    print('You smell gas and jump out through a window.')
    in_house = 0

if not in_house:
    if not player.alive:
        print('\n *** The house claimed your soul. The treasures remain lost. *** ')
    elif len(backpack.contents) != 0:
        print('\n *** You escaped with the following treasure: *** ')
        backpack.contains()
    else:
        print('\n *** Unfortunately, you got out empty-handed. *** ')
