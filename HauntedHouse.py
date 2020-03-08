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
def printRed(text):
    print(colored(text, 'red'))

#CLASSES ARE DEFINED HERE

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
        self.shells = 0
        self.bullets = 6
        self.number_of_keys=0
        self.condition = 'Stable'
        self.weapon = ''
        self.wants_end = 0
        self.in_house = 1
        self.in_room = 0
                
    def __str__(self):
        return ('This ' + self.name + ' has ' + str(self.HP) + ' HP and '+ str(self.AC) + ' AC.') 
    
    def rollsInitiative(self):
        initiative = random.randint(1,21)
        print (' * ' + self.name + ' rolls for initiative, gets ' + str(initiative) + '. *') 
        return initiative 
        
    def isAttacked(self,incoming_hit,incoming_damage):
        if incoming_hit >= self.AC:
            self.HP -= incoming_damage
            print (' * You hit.',self.name + ' takes ' + str(incoming_damage) + ' damage. * ')
            if self.HP <= 0:
                printBold (' * ' + self.name + ' is dead. *')
                self.alive = False
        else:
            print (' * ' + self.name + ' avoids the attack. *')
    
    def isStunned(self):
        print (' * ' + self.name + ' is STUNNED! Doesn`t attack this turn. *')
        self.stunned = 1
        
    def isImmobilized(self):
        print (self.name + ' is IMMOBILIZED. Can`t chase its opponent.')
        
    def rests(self):
        shortrest = random.randint(6,13)
        self.HP += shortrest
        if self.HP > self.maxHP:
            self.HP = self.maxHP
        print (self.name + ' has rested. Currently has ' + str(self.HP) + ' out of ' + str(self.maxHP) + ' hit points.') 
    
class Player(Entity):
             
    def checksInventory(self):
        backpack.contains()
        if self.number_of_keys >= 4:
            printYellow('''
    As you go over your inventory, you realize you have four ancient keys. 
    You should be able to open the rumored vault now. Only one thing remains. 
    You need to find it.
                        ''')
    def loots(self, container_to_loot):
        if len(container_to_loot) != 0: 
            for item in container_to_loot:
                backpack.add(item)
                if 'Shotgun shell' in item:
                    player.shells += 1
                elif 'Bullet' in item:
                    player.bullets += 1
                elif 'key' in item:
                    self.number_of_keys+=1
            print ('\n -> Stuff moved to your backpack.')
            
    def choosesWeapon(self):
        print('\nYou have the following weapons at your disposal:')
        for key in weapon_arsenal.keys():
            print(key)
        weapon_type = ''
        while weapon_type == '':
            weapon_type = input('Which weapon to use?').lower()
            if weapon_type.startswith('f'): 
                self.weapon = 'Fists'
            elif weapon_type.startswith('a'): 
                self.weapon = 'Axe'
            elif weapon_type.startswith('r'):
                self.weapon = 'Revolver pistol'
                if self.bullets == 0:
                    printRed('Your gun is empty.')
                    weapon_type = ''    
                else:
                    self.weapon = 'Revolver pistol'
            elif weapon_type.startswith('s'): 
                if self.shells == 0: 
                    printRed("Damn, seems you're out of shotgun shells.")
                    weapon_type = ''
                else:
                    self.weapon = 'Shotgun'
            else:
                printRed("You don't have that. Using your fists for now.")
                self.weapon = 'Fists'

    def isAttacked(self,attacker_name,incoming_hit,incoming_damage):
        if incoming_hit >= self.AC:
            self.HP -= incoming_damage
            print('\n * You are hit and take ' + str(incoming_damage) + ' damage. *')
            printGreen('\n * ' + self.name + ', you have ' + str(self.HP) + ' HP left. *')
            if self.HP <= 0:
                print ('\n * ' + self.name + ', you are dead. *')
                self.alive = False
        else:
            print ('\n * ' + attacker_name + ' attacks but you avoid the strike. *')
    
    def rollsInitiative(self):
        initiative = random.randint(1,21)
        print ('\n * ' + self.name + ' rolls for initiative: ' + str(initiative) + '. *') 
        return initiative 
   
    def checksUsables(self):
        #compares backpack contents against a list of usable items
        #modifies has_usables class attribute
        usables = ['Bandage','Flashbang','Hardtack','Antidote','Mysterious glass vial']
        for i in usables:    
            if i in backpack.contents:
                self.has_usables = 1
        if self.has_usables:        
            printGreen('\nUsable items:')
            for i in usables:
                if i in backpack.contents:
                    print (i)
        else:
            print('\n * Whoopsie, you are all out of usable items. * \n')
            self.has_usables = 0
            player.checksStats()
    
    def usesItem(self):
        item_to_use = ''
        while item_to_use == '':
            item_to_use = input('Select item to use, check PST or Close the backpack.').lower()
        if item_to_use.startswith('b') and 'Bandage' in backpack.contents:
            self.HP += random.randint(6,12)
            if self.HP > self.maxHP:
                self.HP = self.maxHP
            printYellow('    You tend to your wounds and are healed to ' + str(self.HP) + ' HP.')
            backpack.remove('Bandage')
        elif item_to_use.startswith('f') and 'Flashbang' in backpack.contents:
            if fighting:
                monster.isStunned()
            else:
                printYellow('\n    The flashbang discharges in your hand leaving you momentarily dazed. Well played.')
            backpack.remove('Flashbang')
        elif item_to_use.startswith('h') and 'Hardtack' in backpack.contents:
            self.HP += 2
            if self.HP > self.maxHP:
                self.HP = self.maxHP
            printYellow('\n    The hardtack tastes bland but you recover some strength.')
            backpack.remove('Hardtack')
        elif item_to_use.startswith('a') and 'Antidote' in backpack.contents:
            if self.condition == 'Poisoned':
                self.condition = 'Stable'
                printYellow('\n    The antidote is working. You feel better immediately.')
            else: printYellow('\n    The liquid tastes funny but does nothing.')
            backpack.remove('Antidote')
        elif item_to_use.startswith('m'):
            printYellow('\n    You drink the unknown liquid and taste death. Everything fades to black.')
            backpack.remove('Mysterious glass vial')
            player.alive, player.in_room, player.in_house,player.wants_end = False,0,0,1
        elif item_to_use.startswith('p'):
            player.checksStats()
        elif item_to_use.startswith('c'):
            pass
        else: 
            print('***Item not usable.***')
            
    def checksStats(self):
        printGreen('Your PST reads:')
        printGreen('Health: ' + str(player.HP) +'/'+ str(player.maxHP) + ' | Heart BPM: ' + str(random.randint(120,180)) + '| Condition: ' + player.condition)
    
    def firesShotgun(self):
        player.shells-=1
        backpack.contents.remove('Shotgun shell')
        backpack.add('Spent shell')
    
    def firesPistol(self):
        player.bullets -= 1
class Container:
#container can be filled with items, trapped, hiding a key and looted by player
    def __init__(self,name):
        self.name = name
        self.contents = []
        
    def contains(self):
        if self.contents != []:
            printUnder('\n' + self.name + ' contains:\n')
            for item in self.contents:
                if 'key' in item:
                    print(colored(item, 'yellow'))
                elif 'Bandage' in item or 'Hardtack' in item or 'Antidote' in item:
                    print(colored(item, 'blue'))
                elif 'Flashbang' in item or 'Shotgun shell' in item or 'Bullet' in item or 'vial' in item:
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
            printRed('The '+ self.name + ' is trapped!')
            traps = {'Dart trap':4, 'Poison gas':8, 'Explosion':12}
            #isAttacked(self,attacker_name,incoming_hit,incoming_damage)
            #incoming_hit is randrange
            #incoming_dmg is tied to randomly chosen element from dict traps
            player.isAttacked(random.choice(list(traps.keys())),
                               random.randrange(10,15), traps[random.choice(list(traps.keys()))])
            if not player.alive:
                player.in_room, player.in_house = 0,0
                                  
    def hidesKey(self):
        key_types = ['Brass key', 'Silver key', 'Copper key', 'Iron key']
        if random.randrange(1,100) < 30 and len(key_types)!=0:
            type_of_key = random.choice(key_types)
            self.contents.append(type_of_key)
            key_types.remove(type_of_key)
            
class Location:
#locations are created with empty self.containers
#which are filled by whatInRoom()
    def __init__(self,name):
        self.name = name
        self.container0 = ''
        self.container1 = ''
        self.container2 = ''
        self.container3 = ''
        self.container4 = ''
        self.description = ''
        self.containers = []
        self.conts_abb = []
        self.conts_list = []

    def __str__(self):
        return self.name

    def isEntered(self):
        player.in_room = 1
        printYellow(self.description)
        
    def hasEnemy(self):    
        creatures = ['Groggy ghost','Blob of goo','Ghoul','Poltergeist',
                     'Ghastly pirate','Sad vampire','Lidless eye','Moaning monster',
                     'Chucking woodchuck','Batswarm','Striga','Besny havko',
                     'Creepy doll','Axe murderer','Norman Bates','Starving servant'
                    ]
        monster = Entity(random.choice(creatures),18,10)
        printYellow('    After entering the ' + self.name + ', you are attacked by a '+ monster.name +'.')
        fighting = 1
        player.choosesWeapon()
        return monster,fighting
    
    def whatInRoom(self,item_dic):   
    # argument is a disctionary of self.containers and their items - up to 4 self.containers and no limit on number of items
    # {'CONTAINER':['ITEM1','ITEM2','ITEM3',...]}
    # keys in item_dic should not start with the same letter or letter B,R,E    
        
        for key in item_dic.keys(): self.containers.append(key), self.conts_list.append(key), self.conts_abb.append(key[0].lower())
        self.conts_abb += ['b','r','e']
        try:
            self.container0 = Container(self.containers[0])
            self.container0.hidesKey()
            for item in item_dic[self.containers[0]]:
                self.container0.add(item)        
        except IndexError: pass
        try:
            self.container1 = Container(self.containers[1])
            self.container1.hidesKey()
            for item in item_dic[self.containers[1]]:
                self.container1.add(item)
        except IndexError: pass
        try:
            self.container2 = Container(self.containers[2])
            self.container2.hidesKey()
            for item in item_dic[self.containers[2]]:
                self.container2.add(item)
        except IndexError: pass
        try:
            self.container3 = Container(self.containers[3])
            self.container3.hidesKey()
            for item in item_dic[self.containers[3]]:
                self.container3.add(item)
        except IndexError: pass    
       
    def isExplored(self):
        while player.in_room:
            if len(self.conts_list) != 0:
                printUnder('\nThe following objects catch your eye:\n')
                for c in self.containers: print(c)
                print('\nYou can also check your Backpack, push on to another Room or Escape screaming.')

            else:
                printYellow('\n    This room seems empty. Want to rummage through your Backpack or explore other Rooms?')
            room_choice = input().lower()
            while room_choice == '' or room_choice[0] not in self.conts_abb:
                room_choice = input('The surrounding space gives you chills. What do you do?').lower()
            try:    
                if room_choice[0] == self.containers[0][0].lower():
                    self.container0.is_trapped()
                    if not player.alive: 
                        player.in_room, player.in_house = 0,0
                        break 
                    self.container0.contains()
                    player.loots(self.container0.contents)
                    self.container0.is_looted()
                    self.containers[0] = '' 
                    self.conts_list.remove(self.container0.name) 
            except IndexError: pass
            try:
                if room_choice[0] == self.containers[1][0].lower():
                    self.container1.is_trapped()
                    if not player.alive: 
                        player.in_room, player.in_house = 0,0
                        break
                    self.container1.contains()
                    player.loots(self.container1.contents)
                    self.container1.is_looted()
                    self.containers[1] = ''  
                    self.conts_list.remove(self.container1.name)
            except IndexError: pass
            try:
                if room_choice[0] == self.containers[2][0].lower():
                    self.container2.is_trapped()
                    if not player.alive: 
                        player.in_room, player.in_house = 0,0
                        break
                    self.container2.contains()
                    player.loots(self.container2.contents)
                    self.container2.is_looted()
                    self.containers[2] = ''
                    self.conts_list.remove(self.container2.name)
            except IndexError: pass
            try:
                if room_choice[0] == self.containers[3][0].lower():
                    self.container3.is_trapped()
                    if not player.alive: 
                        player.in_room, player.in_house = 0,0
                        break
                    self.container3.contains()
                    player.loots(self.container3.contents)
                    self.container3.is_looted()
                    self.containers[3] = ''
                    self.conts_list.remove(self.container3.name)
            except IndexError: pass
            if room_choice[0] == 'b':
                player.checksInventory()
                player.checksUsables()
                if player.has_usables:
                    player.usesItem()
            if room_choice[0] == 'r':
                room_exit_lines = ['\n    You push your luck and face another mystery.', 
                            '\n    You leave the area and journey deeper into the house.',
                            '\n    Full of hopes, you carry on.',
                            '\n    You continue exploring.',
                            '\n    Your footsteps echo in the quiet interior.']     
                room_exit_line = random.choice(room_exit_lines)
                printYellow(room_exit_line)
                player.in_room = 0
                if player.condition == 'Poisoned':
                    printBold(colored('\n    The poison takes its toll. You feel your life energy draining.','red'))
                    player.HP -= 3
                    if player.HP <= 0:
                        print (' * ' + self.name + ', you succumb to the toxic substance coursing in your veins. *')
                        player.alive = False
                        player.in_room, player.in_house = 0,0
            if room_choice == 'e':
                player.in_room, player.in_house, player.wants_end = 0,0,1
                printYellow('    Smart. You left the house. Fresh air caresses your face once again.')       

#ROUND OF COMBAT IS DEFINED HERE
#in game is looping while player or enemy is alive

def combat(player,monster,fighting):
	#if player chose shotgun or pistol, checks for ammo, lets him choose again
    if player.weapon == 'Shotgun' and player.shells == 0:
        printRed('You spent all of your shells. Need to quickly swap weapons.')
        player.choosesWeapon()
    if player.weapon == 'Revolver pistol' and player.bullets == 0:
        printRed('You spent all of your bullets. Quickly swapping weapons.')
        player.choosesWeapon()
    #every round of combat starts with initiative
    if int(player.rollsInitiative()) > int(monster.rollsInitiative()):
        print ('\nYou react faster.')
        ###if player wins initiative, lets him choose to fight or check inventory and use item
        if input('\nFight or Use item?').lower().startswith('f'):
            monster.isAttacked(13,random.randint(weapon_arsenal[player.weapon][0],weapon_arsenal[player.weapon][1]))
            if player.weapon == 'Shotgun': player.firesShotgun()
            elif player.weapon== 'Revolver pistol': player.firesPistol()
            if not monster.alive:
                fighting = 0
            else:
                player.isAttacked(monster.name,random.randint(5,15),random.randint(2,10))
                if not player.alive:
                    fighting = 0    
        else:
            player.checksUsables()
            if player.has_usables:
                player.usesItem()
            if monster.stunned:
                monster.isAttacked(11,random.randint(weapon_arsenal[player.weapon][0],weapon_arsenal[player.weapon][1]))
                if player.weapon == 'Shotgun': player.firesShotgun()
                elif player.weapon == 'Revolver pistol': player.firesPistol()
                if not monster.alive:
                    fighting = 0
            else:
                player.isAttacked(monster.name,random.randint(5,15),random.randint(2,10))
                if not player.alive:
                    fighting = 0
    else:
        print ('\n' + monster.name + ' is too quick for you.')
        player.isAttacked(monster.name,random.randint(5,15),random.randint(2,10))
        if not player.alive:
            fighting = 0
        else:
            monster.isAttacked(11,random.randint(weapon_arsenal[player.weapon][0],weapon_arsenal[player.weapon][1]))
            if player.weapon == 'Shotgun': player.firesShotgun()
            elif player.weapon == 'Revolver pistol': player.firesPistol()
            if not monster.alive:
                fighting = 0
    return player,monster,fighting
                         
#LOCATIONS ARE DEFINED HERE

foyer = Location('Foyer')
foyer.description = '''
    You enter the Foyer and immediatly realize you are definitely the first guest 
    to do so after very many years. Dust covers every nook and cranny, 
    the floral-patterned drapes are long gone, succeeded by strips 
    of moth-eaten cloth ominously moving in the cold breeze 
    you let in through the front door. 
    The smell of mildew attacks your nostrils. 
    '''
foyer.whatInRoom({'Painting of lady and lord Durst':['Bleached letter'],
                'Wardrobe':['Bandage','Dusty duster']
               })
grandHall = Location('Grand hall')
grandHall.description = '''
    You find yourself in a huge open space. The floor is marble, the walls covered in wooden mosaic tiles.
    A wide gallery runs around the hall on the second floor and a majestic chandelier hangs above your head.
    However, the lightbulbs are long gone and shadows reign all around.
    '''
grandHall.whatInRoom({'Weapon cabinet':['Flashbang','Rusty nail','Shotgun shell'],
                'Iron lockbox':['Bag of coins','Polished emerald'],
                'Antique vase':['Dried tulips','Wasp nest']
               })
kitchen = Location('Kitchen')
kitchen.description = '    You enter the Kitchen and smell stew cooking. And something else, too. Is it burning hair?'
kitchen.whatInRoom({'Shabby cupboard':['Bandage','Worm-ridden bag of flour'],
                'Wooden box':['Sack of turnips','Bunch of carrots'],
                'Kitchen counter':['Severed head of lady Durst']
               })
longHallway = Location('Long hallway')
longHallway.descritpion = '''
    Walking along a carpeted hallway you notice a secret compartment behind a rotten wallpaper.
    '''
longHallway.whatInRoom({'Painting of a landscape':['"Merry marshes" by Catherine Durst: oil on canvas'],
                'Secret stash':['Huge ruby','Bloody ringfinger','Bullet'],
                'First aid lockbox':['Bandage','Bandage','Antidote']
               })
gallery = Location('Gallery')
gallery.description ='''

    '''
gallery.whatInRoom({'Huge cocoon':['Slimy eggsack','Half-digested cat'],
                'Small cocoon':['Black sludge'],
                'Web-covered display case':['Shotgun shell','Ceremonial dagger','Tribal leather bracelet'],
                'Loose brick':['Dead rat']
                })
study = Location('Study')
study.description ='''
    The Study greets you with a smell of old parchment and cinnamon. Shelves full of leather-bound books 
    line the walls, the massive oaken table is covered with dripped candle wax. You walk across the Study
    on a thick red carpet.
    '''
study.whatInRoom({'Painting of a city panorama':['"Smothering smog" by Catherine Durst: oil on canvas'],
                'Iron lockbox':['Shotgun shell','Bullet','Bullet','Steel arrowhead'],
                'Shelves':['"The king in yellow"','"Victorian handbook of poisons"']
                }) 
vault = Location('Vault')
vault.description = '''
    You enter a large room dominated by magnificient steel doors. This has to be the vault. You see four 
    keyholes before you.
    '''
vault.whatInRoom({'Old pouch':['Strange rune']
                }) 
safe = Location('Safe')
safe.description = '    You enter the safe.'
safe.whatInRoom({'Glass display case':['Strange clockwork device'],
                            'Ornate display case':['Jade statue'],
                            'Treasure chest':['Pile of gold coins','Assortment of precious stones'],
                            'Stone coffin':['Remains of Catherine Durst','Blood-soaked handkerchief']
                           }) 
basement = Location('Basement')
basement.description = '''
    The basement is soaked in darkness. You can make out shapes, but can not discern what surrounds you.
    '''







#GAMEPLAY STARS HERE

printBold('Barry the Butler says: "Welcome to the haunted house."')
printBold('Barry the Butler says: "How would you like to be addressed?."')
player_name = input()
player = Player(player_name, 50, 12)
backpack = Container('Backpack')
backpack.add('PST: Personal Statistics Tracker')
printBold('Barry the Butler says: "' + player.name + ', the house holds many treasures."')
printBold('''
Barry the Butler says: "To navigate the premises and carry out actions, just type the capitalized letters.
                        Notice that not all items are usable - when inspecting your inventory, 
                        usable items will be highlighted."''')

printBold('''
Barry the Butler says: "And if you`re looking for the vault, be warned - you need to collect 4 keys.'
                        The keys, while not directly usable, are highlighted in yellow."''')
printBold('Barry the Butler says: "Enjoy your stay."')
player.in_house = 1
weapon_arsenal = {'Fists':[1,6], 
                  'Axe':[4,10],
                  'Revolver pistol':[10,16],
                  'Shotgun':[18,20]}
while player.in_house and player.alive:
    foyer.isEntered()
    foyer.isExplored()
    if player.wants_end: break
    
    grandHall.isEntered()
    monster, fighting = grandHall.hasEnemy() 
    while fighting:
        player,monster,fighting = combat(player,monster,fighting)
    if not player.alive: break
    grandHall.isExplored()
    if player.wants_end: break
    
    kitchen.isEntered()
    monster,fighting = kitchen.hasEnemy() 
    while fighting:
        player,monster,fighting = combat(player,monster,fighting)
    if not player.alive: break  
    kitchen.isExplored()
    if player.wants_end: break
    
    longHallway.isEntered()
    longHallway.isExplored()
    if player.wants_end: break
    
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
                player.choosesWeapon()
                while fighting:
                    player,monster,fighting = combat(player,monster,fighting)
                if not player.alive:
                    in_hallway = 0
                    player.in_house,player.wants_end = 0,1
                    break
                else:
                    printYellow('''
    The beast lies in a pool of its own blood. In the far corner of the cage
    you notice a ragged backpack. Must've belonged to a previous explorer.
                        ''')
                    oldBackpack = Container('Old backpack')
                    oldBackpack.hidesKey()
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
    if player.wants_end: break        
  
    printYellow('''
    After you catch your breath you realize you arrived to the gallery
    overlooking the grand hall. The space around you is dominated by thick spiderwebs. 
                ''')
    on_gallery = 1
    gallery_items = ['Twitching cocoon', 'Discarded flashbang']
    gallery_choice_potential = ['t','d','r']
    while on_gallery:
        printUnder('\nThe following objects catch your eye:\n')
        for item in gallery_items:
            if 'flashbang' in item: print(colored(item, 'red'))
            else: print(item)    
        print('Alternatively, you can get Ready and go on exploring this floor.')
        gallery_choice = input().lower()
        while gallery_choice == '' or gallery_choice not in gallery_choice_potential:
            gallery_choice = input(' * The human-sized cocoon continues twitching. * ').lower()
        if gallery_choice.startswith('d'):
            backpack.add('Flashbang')
            printYellow("    Someone tried and failed to use this flashbang. It will serve you well.")
            gallery_choice_potential.remove('d')
            gallery_items.remove('Discarded flashbang')
        elif gallery_choice.startswith('t'):
            printYellow('''
            You approach the strange cocoon. The closer you get the more it resembles
            a human shape. You could swear you hear a soft moaning. A plea for help?
            You hold your breath and touch it. It burst under a sudden pressure from within
            and sprays you with a caustic liquid. A swarm of ferocious spiders 
            starts crawling up your hand. Disgusting.
                        ''')
            player.condition = 'Poisoned'
            monster = Entity('Spider swarm',20,1)
            fighting = 1
            player.choosesWeapon()
            while fighting:
                player,monster,fighting = combat(player,monster,fighting)
            if not player.alive:
                player.in_house, player.wants_end = 0,1
                break
            else:
                printYellow('''
    The spiders are gone. For now. However, you don't feel quite well.
                         ''')
                break
        elif gallery_choice.startswith('r'):
            break
    gallery.isExplored()
    if player.wants_end: break
    
    printYellow('''
    Walking along the gallery you catch movement in the corner of your eye. 
    Want to Investigate or Leave?
                ''')
    hallway_choice = input().lower()
    while hallway_choice == '' or hallway_choice[0] not in ['i','l']:
        hallway_choice = input(' * The spiderwebs around you are starting to vibrate. *').lower()
    if hallway_choice[0] == 'i':
        monster = Entity('Savage spider',14,8)
        printYellow('\n    An enormous spider moves towards you with lightning speed.')
        fighting = 1
        player.choosesWeapon()
        while fighting:
            player,monster,fighting = combat(player,monster,fighting)
        if not player.alive:
            in_hallway = 0
            player.in_house, player.wants_end = 0,1
            break
        else:
            printYellow('''
    The spider's body twitches even after the beast's death. 
    As you slice open its abdomen, you find one of the ancient keys.                             
                ''')
            backpack.add('Ancient key')
    else:
        printYellow('    Better safe than sorry. You quicken your pace.')
    
    study.isEntered()
                
    printYellow('    You are startled by a sudden opening of the study doors. The butler enters.')
    printBold('''
Barry the Butler says:"I see you are still alive. The vault awaits behind the next door.
                       It is dangerous to go alone, take this."
                            ''')
    printYellow('    He hands you a small glass vial, chuckles ominously and disappears in a puff of smoke.')
    backpack.add('Mysterious glass vial')
    study.isExplored()
    if player.wants_end: break
        
    vault.isEntered()
    vault.isExplored()
    if player.number_of_keys == 4:
        printYellow('''
        One by one you open all the locks. Gears start to turn inside the walls 
        and hidden machinery comes alive. The doors start to open slowly.
                    ''')
        safe.isEntered
        safe.isExplored
        
        if player.wants_end: break
        print('''
    As you loot the safe a terrible feeling fills your mind. It seems your mere presence 
    awakened something ancient in the bowels of the house. The very foundations of the building 
    are shaking, the walls are cracking and debris is crashing down all around you. 
    You look for a possible exit and find a hidden staircase leading down.    
              ''')
    else:
        printYellow('''
    You are missing the necessary keys and are not able to open all of the locks. 
    More exploring is necessary. However, it seems your mere presence awakened something 
    ancient in the bowels of the house. The very foundations of the building are shaking, 
    the walls are cracking and debris is crashing down all around you. You look for a possible exit
    and find a hidden staircase leading down.)
                    ''')
    basement.isEntered()

#TODO: forced game over here, add more content    
    print('>>>>The shadows around you coalesce into claws. Fortunately, you spot a small window, squeeze through and escape the house.<<<<')
    player.in_house = 0

if not player.in_house:
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

