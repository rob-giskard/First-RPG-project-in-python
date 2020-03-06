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
        self.shells = 0
        self.bullets = 6
        self.number_of_keys=0
        self.condition = 'Stable'
        self.weapon = ''
        
    def __str__(self):
        return ('This ' + self.name + ' has ' + str(self.HP) + ' HP and '+ str(self.AC) + ' AC.') 
    
    def rolls_initiative(self):
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
            
    def chooses_weapon(self):
        
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
                    print('Your gun is empty.')
                    weapon_type = ''    
                else:
                    self.weapon = 'Revolver pistol'
            elif weapon_type.startswith('s'): 
                if self.shells == 0: 
                    print ("Damn, seems you're out of shotgun shells.")
                    weapon_type = ''
                else:
                    self.weapon = 'Shotgun'
            else:
                print("You don't have that. Using your fists for now.")
                self.weapon = 'Fists'

    def isAttacked(self,attacker_name,incoming_hit,incoming_damage):
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
                monster.is_stunned()
            else:
                printYellow('    The flashbang discharges in your hand leaving you momentarily dazed. Well played.')
            backpack.remove('Flashbang')
        elif item_to_use.startswith('h') and 'Hardtack' in backpack.contents:
            self.HP += 2
            if self.HP > self.maxHP:
                self.HP = self.maxHP
            printYellow('    The hardtack tastes bland but you recover some strength.')
            backpack.remove('Hardtack')
        elif item_to_use.startswith('a') and 'Antidote' in backpack.contents:
            if self.condition == 'Poisoned':
                self.condition = 'Stable'
                print('The antidote is working. You feel better immediately.')
            else: print('The liquid tastes funny but does nothing.')
            backpack.remove('Antidote')
        elif item_to_use.startswith('m'):
            printYellow(    'You drink the unknown liquid and taste death. Everything fades to black.')
            backpack.remove('Mysterious glass vial')
            player.alive = False
            in_room, in_house, end_it = 0,0,1
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
#blueprint for a container
    def __init__(self,name):
        self.name = name
        self.contents = []
        
    def contains(self):
        if self.contents != []:
            printUnder(self.name + ' contains:\n')
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
            print('The '+ self.name + ' is trapped!')
            traps = {'Dart trap':4, 'Poison gas':8, 'Explosion':12}
            #isAttacked(self,attacker_name,incoming_hit,incoming_damage)
            #incoming_hit is randrange
            #incoming_dmg is tied to randomly chosen element from dict traps
            player.isAttacked(random.choice(list(traps.keys())),
                               random.randrange(10,15), traps[random.choice(list(traps.keys()))])
    def hides_key(self):
        if random.randrange(1,100) < 30:
            key_types = ['Brass key', 'Gold key', 'Silver key', 'Copper key', 'Iron key', 'Tin key']
            type_of_key = random.choice(key_types)
            self.contents.append(type_of_key)
            
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
        player.chooses_weapon()
        return monster,fighting
    
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
                printUnder('\nThe following objects catch your eye:\n')
                for key in item_dic.keys(): print(key)
                print('Alternatively, you can check your Backpack, push on to another Room or Escape screaming.')

            else:
                printYellow('    This room seems empty. Want to rummage through your Backpack or explore other Rooms?')
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
                in_room = 0
                if player.condition == 'Poisoned':
                    printBold(colored('\n    The poison takes its toll. You feel your life energy draining.','red'))
                    player.HP -= 3
                    if player.HP <= 0:
                        print (' * ' + self.name + ', you succumb to the toxic substance coursing in your veins. *')
                        player.alive = False
                        in_room, in_house, end_it = 0,0,1
            if room_choice == 'e':
                in_room, in_house, end_it = 0,0,1
                printYellow('    Smart. You left the house. Fresh air caresses your face once again.')
        

def combat(player,monster,fighting):
	
        if player.weapon == 'Shotgun' and player.shells == 0:
            print('You spent all of your shells. Need to quickly swap weapons.')
            player.chooses_weapon()
        if player.weapon == 'Revolver pistol' and player.bullets == 0:
            print('You spent all of your bullets. Quickly swapping weapons.')
            player.chooses_weapon()
        
        if int(player.rolls_initiative()) > int(monster.rolls_initiative()):
            print ('\nYou react faster.')
            ###if player wins initiative, let him choose to fight or check inventory and use item
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
in_house = 1
end_it = 0
weapon_arsenal = {'Fists':[1,6], 
                          'Axe':[4,10],
                          'Revolver pistol':[10,16],
                          'Shotgun':[18,20]}
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
    ''')
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
    monster, fighting = room2.has_enemy() 

    while fighting:
        player,monster,fighting = combat(player,monster,fighting)
    if not player.alive:
        in_house = 0
        break
    room2.what_in_room({'Weapon cabinet':['Flashbang','Rusty nail','Shotgun shell'],
                'Iron lockbox':['Bag of coins','Polished emerald'],
                'Antique vase':['Dried tulips','Wasp nest']
               })
    if end_it: break
    room3 = Location('Kitchen')
    printYellow('    You enter the Kitchen and smell stew cooking. And something else, too. Is it burning hair?')
    monster,fighting = room3.has_enemy() 

    while fighting:
        player,monster,fighting = combat(player,monster,fighting)
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
                'Secret stash':['Huge ruby','Bloody ringfinger','Bullet'],
                'First aid lockbox':['Bandage','Bandage','Antidote']
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
                player.chooses_weapon()
                while fighting:
                    player,monster,fighting = combat(player,monster,fighting)
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
    on_gallery = 1
    printYellow('''
    After you catch your breath you realize you arrived to the gallery
    overlooking the grand hall. The space around you is dominated by thick spiderwebs. 
                ''')
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
            player.chooses_weapon()
            while fighting:
                player,monster,fighting = combat(player,monster,fighting)
            if not player.alive:
                in_house = 0
                end_it = 1
                break
            else:
                printYellow('''
        The spiders are gone. For now. However, you don't feel quite well.
                         ''')
                break
        elif gallery_choice.startswith('r'):
            break
    room4.what_in_room({'Huge cocoon':['Slimy eggsack','Half-digested cat'],
                'Small cocoon':['Black sludge'],
                'Web-covered display case':['Shotgun shell','Ceremonial dagger','Tribal leather bracelet'],
                'Loose brick':['Dead rat']
                })
    if end_it: break
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
        player.chooses_weapon()
        while fighting:
            player,monster,fighting = combat(player,monster,fighting)
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
            backpack.add('Ancient key')
    else:
        printYellow('    Better safe than sorry. You quicken your pace.')
    room5 = Location('Study')
    printYellow('''
    The Study greets you with a smell of old parchment and cinnamon. Shelves full of leather-bound books 
    line the walls, the massive oaken table is covered with dripped candle wax. You walk across the Study
    on a thick red carpet.
                ''')
    printYellow('    You are startled by a sudden opening of the study doors. The butler enters.')
    printBold('''
Barry the Butler says:"I see you are still alive. The vault awaits behind the next door.
                       It is dangerous to go alone, take this."
                            ''')
    printYellow('    He hands you a small glass vial, chuckles ominously and disappears in a puff of smoke.')
    backpack.add('Mysterious glass vial')
    room5.what_in_room({'Painting of a city panorama':['"Smothering smog" by Catherine Durst: oil on canvas'],
                'Small lockbox':['Shotgun shell','Bullet','Bullet','Steel arrowhead'],
                'Shelves':['"The king in yellow"','"Victorian handbook of poisons"']
               }) 
    if end_it: break
        
    room6 = Location('Vault')
    printYellow('''
    You enter a large room dominated by magnificient steel doors. This has to be the vault. You see four 
    keyholes before you.
                ''')
    if player.number_of_keys >= 4:
        printYellow('''
        One by one you open all the locks. Gears start to turn inside the walls 
        and hidden machinery comes alive. The doors start to open slowly.
                    ''')
        room6.what_in_room({'Glass display case':['Strange clockwork device'],
                            'Ornate display case':['Jade statue'],
                            'Treasure chest':['Pile of gold coins','Assortment of precious stones'],
                            'Stone coffin':['Remains of Catherine Durst','Blood-soaked handkerchief']
                           }) 
        if end_it: break
        print('''
    As you loot the vault a terrible feeling fills your mind. It seems your mere presence 
    awakened something ancient in the bowels of the house. The very foundations of the building 
    are shaking, the walls are cracking and debris is crashing down all around you. 
    You look for a possible exit and find a hidden staircase leading down.)    
              ''')
    else:
        printYellow('''
    You are missing the necessary keys and are not able to open all of the locks. 
    More exploring is necessary. However, it seems your mere presence awakened something 
    ancient in the bowels of the house. The very foundations of the building are shaking, 
    the walls are cracking and debris is crashing down all around you. You look for a possible exit
    and find a hidden staircase leading down.)
                    ''')
    
    room7 = Location('Basement')
    
    print('>>>>The shadows around you coalesce into claws. Fortunately, you spot a small window, squeeze through and ascape the house.<<<<')
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

