import random
import sys
from termcolor import colored, cprint

def printBold(text):
    print(colored(text,attrs=['bold']))
def printUnder(text):
    print(colored(text,attrs=['underline']))
def printYellow(text):
    print(colored(text, 'yellow'))
def printGreen(text):
    print(colored(text, 'green'))
    
class Entity:
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
        print (' * ' + self.name + ' rolls for initiative, gets ' + str(initiative) + '. *') 
        return initiative 
        
    def is_attacked(self,incoming_hit,incoming_damage):
        if incoming_hit >= self.AC:
            self.HP -= incoming_damage
            print (' * You hit.',self.name + ' takes ' + str(incoming_damage) + ' damage. * ')
            if self.HP <= 0:
                printBold (' * ' + self.name + ' is dead. *')
                self.alive = False
        else:
            print (' * ' + self.name + ' avoids the attack. *')
    
    def is_stunned(self):
        print (' * ' + self.name + ' is STUNNED! Doesn`t attack this turn. *')
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
            printYellow('''
    As you go over your inventory, you realie you have four ancient keys. 
    You should be able to open the rumored vault now. Only one thing remains. 
    You need to find it.
                        ''')
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
            print('\n * You are hit and take ' + str(incoming_damage) + ' damage. *')
            printGreen(' * ' + self.name + ', you have ' + str(self.HP) + ' HP left. *')
            if self.HP <= 0:
                print (' * ' + self.name + ', you are dead. *')
                self.alive = False
        else:
            print (' * ' + attacker_name + ' attacks but you avoid the strike. *')
    def rolls_initiative(self):
        initiative = random.randint(1,21)
        print ('\n * ' + self.name + ' rolls for initiative: ' + str(initiative) + '. *') 
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
            print('\n * Whoopsie, you are all out of usable items. * \n')
            self.has_usables = 0
            player.checksStats()
            
      
    
    def uses_item(self):
        item_to_use = ''
        while item_to_use == '':
            item_to_use = input('Select item to use, check PST or Close the backpack.').lower()
        if item_to_use.startswith('b') and 'Bandage' in backpack.contents:
            self.HP += random.randint(6,12)
            if self.HP > self.maxHP:
                self.HP = self.maxHP
            print (' * You are healed to ' + str(self.HP) + ' HP. *')
            backpack.remove('Bandage')
        elif item_to_use.startswith('f') and 'Flashbang' in backpack.contents:
            if fighting:
                monster.is_stunned()
            else:
                printYellow('    The flashbang discharges in your hand leaving you momentarily dazed. Well played.')
            backpack.remove('Flashbang')
        elif item_to_use.startswith('p'):
            player.checksStats()
        elif item_to_use.startswith('c'):
            pass
        else: 
            print('Not usable.')
            
    def checksStats(self):
        printGreen('Your PST reads:')
        printGreen('Health: ' + str(player.HP) +'/'+ str(player.maxHP) + ' | Heart BPM: ' + str(random.randint(120,180)))
    
class Container:
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
class Location:
# instances of this class are created with a name of the room
# and an indicator of danger
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
        printYellow('    After entering the ' + self.name + ', you are attacked by a '+ monster.name +'.')
        fighting = 1
        max_weapon_damage = player.chooses_weapon()
        return monster,fighting,max_weapon_damage
    
    def what_in_room(self,item_dic):   
    # deals with player choice, keys, trapped containers and looting 
    # before calling this function, need to fill given containers, place keys
    # argument is a disctionary of containers and their items - up to 4 containers and no limit on number of items
    # 'CONTAINER':'ITEM1','ITEM2','ITEM3',...
    # keys in item_dic should not start with the same letter
    
        global in_house
        global end_it 
        in_room = 1
        containers = []
        conts_abb = []
        for key in item_dic.keys(): containers.append(key), conts_abb.append(key[0].lower())
        conts_abb += ['b','r','e']
        try:
            cont0 = Container(containers[0])
            cont0.hides_key()
            for item in item_dic[containers[0]]:
                cont0.add(item)
        except IndexError: pass
        try:
            cont1 = Container(containers[1])
            cont1.hides_key()
            for item in item_dic[containers[1]]:
                cont1.add(item)
        except IndexError: pass
        try:
            cont2 = Container(containers[2])
            cont2.hides_key()
            for item in item_dic[containers[2]]:
                cont2.add(item)
        except IndexError: pass
        try:
            cont3 = Container(containers[3])
            cont3.hides_key()
            for item in item_dic[containers[3]]:
                cont3.add(item)
        except IndexError: pass    

        while in_room:
            if len(containers) !=0:
                print('\nIn this room you can explore:')
                for key in item_dic.keys(): print(key)
                print('Alternatively, you can check your Backpack, push on to another Room or Escape screaming.')

            else:
                print('This room seems empty. Want to rummage through your Backpack or explore other Rooms?')
            room_choice = input().lower()
            while room_choice == '' or room_choice[0] not in conts_abb:
                room_choice = input('The surrounding space gives you chills. What do you do?').lower()
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
                room_exit_lines = ['\n    You push open the door and face another room.', 
                              '\n    You leave the room and journey deeper into the house.',
                              '\n    Full of hopes, you carry on.',
                              '\n    You continue exploring.',
                              '\n    Your footsteps echo in the quiet interior.']     
                room_exit_line = random.choice(room_exit_lines)
                printYellow(room_exit_line)
                in_room = 0
            if room_choice == 'e':
                in_room, in_house, end_it = 0,0,1
                printYellow('    Smart. You left the house. Fresh air caresses your face once again.')
        

def combat(player,monster,fighting,max_weapon_damage):
    
        if int(player.rolls_initiative()) > int(monster.rolls_initiative()):
            print ('\nYou react faster.')
            ###if player wins initiative, let him choose to fight or check inventory and use item
            if input('\nFight or Use item?').lower().startswith('f'):
                monster.is_attacked(11,random.randint(1,max_weapon_damage))
                if not monster.alive:
                    fighting = 0
                else:
                    player.is_attacked(monster.name,random.randint(5,15),random.randint(2,10))
                    if not player.alive:
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
            print ('\n' + monster.name + ' is too quick for you.')
            player.is_attacked(monster.name,random.randint(5,15),random.randint(2,10))
            if not player.alive:
                fighting = 0
            else:
                monster.is_attacked(11,random.randint(1,max_weapon_damage))
                if not monster.alive:
                    fighting = 0
        return player,monster,fighting

#Gameplay begins here            
printBold('Barry the Butler says: "Welcome to the haunted house."')
printBold('Barry the Butler says: "How would you like to be addressed?."')
player_name = input()
player = Player(player_name, 50, 12)
backpack = Container('Backpack')
backpack.add('PST: Personal Statistics Tracker')
printBold('Barry the Butler says: "' + player.name + ', the house holds many treasures."')
printBold('Barry the Butler says: "To navigate the premises and carry out actions, just type the capitalized letters."')
printBold('Barry the Butler says: "And if you`re looking for the vault, be warned - you need to collect 4 keys."')
printBold('Barry the Butler says: "Enjoy your stay."')
number_of_keys = 0
in_house = 1
end_it = 0
while in_house:
    room1 = Location('Foyer')
    printYellow(
    '''
    You enter the Foyer and immediatly realize you are definitely the first guest 
    to do so after very many years. Dust covers every nook and cranny, 
    the floral-patterned drapes are long gone, succeeded by strips 
    of moth-eaten cloth ominously moving in the cold breeze 
    you let in through the front door. 
    The smell of mildew attacks your nostrils. 
    '''
    )
    room1.what_in_room({'Painting of lady and lord Durst':['Bleached letter'],
                'Wardrobe':['Bandage','Dusty duster']
               })
    if end_it: break
    room2 = Location('Grand hall')
    printYellow('''
    You find yourself in a huge open space. The floor is marble, the walls covered in wooden mosaic tiles.
    A wide gallery runs around the hall on the second floor and a majestic chandelier hangs above your head.
    However, the lightbulbs are long gone and shadows reign all around.
                ''')
    monster, fighting,max_weapon_damage = room2.has_enemy() 
    while fighting:
        player,monster,fighting = combat(player,monster,fighting,max_weapon_damage)
    if not player.alive:
        in_house = 0
        break
    room2.what_in_room({'Weapon cabinet':['Flashbang','Rusty nail'],
                'Iron lockbox':['Bag of coins','Polished emerald'],
                'Antique vase':['Dried tulips','Wasp nest']
               })
    if end_it: break
    room3 = Location('Kitchen')
    printYellow('    You enter the Kitchen and smell stew cooking. And something else, too. Is it burning hair?')
    monster,fighting,max_weapon_damage = room3.has_enemy() 
    while fighting:
        player,monster,fighting = combat(player,monster,fighting,max_weapon_damage)
    if not player.alive:
        in_house = 0
        break  
    room3.what_in_room({'Shabby cupboard':['Bandage','Worm-ridden bag of flour'],
                'Wooden box':['Sack of turnips','Bunch of carrots'],
                'Kitchen counter':['Severed head of lady Durst']
               }) 
    if end_it: break
    room4 = Location('Long hallway')
    printYellow('''
    Walking along a carpeted hallway you notice a secret compartment behind a rotten wallpaper.
                ''')
    room4.what_in_room({'Painting of a landscape':['"Merry marshes" by Catherine Durst: oil on canvas'],
                'Secret stash':['Huge ruby','Bloody ringfinger'],
                'First aid lockbox':['Bandage']
               }) 
    if end_it: break
    in_hallway = 1
    printYellow('''
    At the end of the hallway you find two doors. 
    Soft growling can be heard from behind the one on the Left. 
    This door seem to be reinforced with metal sheets. 
    The door on the Right is covered in dark burgundy Spots.  
    ''')
    while in_hallway:
        hallway_choice = input().lower()
        while hallway_choice == '' or hallway_choice[0] not in ['l','r','s']:
            hallway_choice = input(' * The growling intensifies. Something senses your arrival. *').lower()
        if hallway_choice[0] == 'l':
            printYellow('''
    You open the door and find yourself facing a caged animal. 
    It looks like a huge wolf with open wounds on various parts of its body. 
    You could get Closer or Back up to a safe distance.
                ''')                
            what_now = input().lower()
            while what_now == '' or what_now[0] not in ['c','b']:
                what_now = input(' * The monstrous dog watches you with curious eyes. *').lower()
            if what_now[0] == 'b':
                printYellow('    You are back in the hallway.')
            elif what_now[0] == 'c':
                monster = Entity('Hellhound',42,12)
                print('\n * The ' + monster.name + ' was obviously wainting in ambush. It tears open its cage and lunges at you. * ')
                fighting = 1
                max_weapon_damage = player.chooses_weapon()
                while fighting:
                    player,monster,fighting = combat(player,monster,fighting,max_weapon_damage)
                if not player.alive:
                    in_hallway = 0
                    in_house = 0
                    end_it = 1
                    break
                else:
                    printYellow('''
    The beast lies in a pool of its own blood. In the far corner of the cage
    you notice a ragged backpack. Must've belonged to a previous explorer.
                        ''')
                    oldBackpack = Container('Old backpack')
                    oldBackpack.hides_key()
                    oldBackpack.add('Bandage')
                    oldBackpack.add('Shotgun shell')
                    oldBackpack.add('Hardtack')
                    oldBackpack.contains()
                    player.loots(oldBackpack.contents)
                    oldBackpack.is_looted()
                    printYellow('''
    You leave the defeated foe behind, return to the hallway and enter the remaining door.
    A long staircase leads upstairs. Exhausted from the fight you start climbing. 
                    ''')
                    in_hallway = 0
        elif hallway_choice[0] == 's':
            printYellow('    After closer inspection you identify the spots as age-old dried blood.')
        elif hallway_choice[0] == 'r':
            printYellow('''
    You found stairs leading up. The beastial sounds behind your back are getting louder
    every moment. You don't have time to think and rush upstairs.
                        ''')
            in_hallway = 0
    if end_it: break        
    room4 = Location('Gallery')
    printYellow('''
    After you catch your breath you realize you arrived to the gallery
    overlooking the grand hall. The space around you is dominated by thick spider-webs. 
                ''')
    room2.what_in_room({'Huge cocoon':['Slimy eggsack','Half-digested cat'],
                'Small cocoon':['Black sludge'],
                'Web-covered display case':['Shotgun shell','Ceremonial dagger','Tribal leather bracelet'],
                'Loose brick':['Dead rat']
                })
    if end_it: break
    printYellow('''
    Walking along the gallery you catch a movement in the corner of your eye. 
    Want to Investigate or Leave?
                ''')
    hallway_choice = input().lower()
    while hallway_choice == '' or hallway_choice[0] not in ['i','l']:
        hallway_choice = input(' * The spider-webs around you are starting to vibrate. *').lower()
    if hallway_choice[0] == 'i':
        monster = Entity('Savage spider',26,12)
        print('\n    An enormous spider moves towards you with lightning speed.')
        fighting = 1
        max_weapon_damage = player.chooses_weapon()
        while fighting:
            player,monster,fighting = combat(player,monster,fighting,max_weapon_damage)
        if not player.alive:
            in_hallway = 0
            in_house = 0
            end_it = 1
            break
        else:
            printYellow('''
    The spider's body twitches even after the beast's death. 
    As you slice open its abdomen, you find one of the ancient keys.                             
                ''')
    else:
        printYellow('    Better safe than sorry. You continue to another door.')
        
    
            
    print('>>>>You smell gas and jump out through a window.<<<<')
    in_house = 0

if not in_house:
    if not player.alive:
        print('\n *** The house claimed your soul. The treasures remain lost. *** ')
    elif len(backpack.contents) > 1:
        print('\n *** You escaped with the following treasure: *** ')
        for item in backpack.contents:
            if item == 'PST: Personal Statistics Tracker':
                continue
            else:
                print(item)
    else:
        print('\n *** Unfortunately, you got out empty-handed. *** ')



#TODO help text
#TODO shotgun shells
#TODO: score count, points for every item





