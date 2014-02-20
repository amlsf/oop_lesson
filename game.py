"""
More interestingly, spend some time playing with object interactions, adding more objects and classes to your game, and fixing some bugs. Here are some ideas:

Fix the game so it doesn't crash when you go beyond the game board boundaries.
Add other elements to the game, keys, chests, doors
Add conditional interactions: a door that won't open unless you have the right colored gem, chests that won't open unless you have the right key.
Subclass the Character class to make non-player characters that speak messages when you interact with them.
Tricky: Add blocks that slide when you push them.
"""


import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 12

#### Put class definitions here ####

# Creates Player Character ot interact with, only instantiated once (not Non-Player Characters)
class Character(GameElement):
    IMAGE = "Horns"

    # Makes Character Class able to recognize own position, encapsulating behavior. Tells direction to go in and is referenced in keyboard_handler function
    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
#TODO Why do we need this return Non below here? Seems to work fine in the "if direction statement below"            
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

class SubCharacter(Character):
    IMAGE = "Cat"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("How are you doing today?")

# Creates rock instances of Rock class
# TODO is Rock a subclass of Subelement that inherits all its properties? 
class Rock(GameElement):
    # Pulls image nicknamed Rock from setup_images function in engine.py
    IMAGE = "Rock"
    # creates solid attribute so don't have to check if various elements for walking through
    SOLID = True

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %r items! Your inventory is %r" % (len(player.inventory), player.inventory))

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    LOCKED = True

    def interact(self, player):
    # TODO handle for nothing in list

        if player.inventory == []:
            GAME_BOARD.draw_msg("Your inventory is empty! You need a specific key to open this door")
        else: 
            for item in player.inventory:   
                if type(item) == Key and item.KEY == 1:
                    GAME_BOARD.del_el(self.x, self.y)
            # if key in inventory, change door to non-solid open door
                    GAME_BOARD.draw_msg("Congratulations! You have acquired the correct key to open this door")
                    opendoor1 = OpenedDoor()
                    GAME_BOARD.register(opendoor1)
                    GAME_BOARD.set_el(self.x, self.y, opendoor1)
                else: 
                    GAME_BOARD.draw_msg("You do not have a right key to unlock this door!")

# TODO how to not make the door disappear when walk through it?
class OpenedDoor(GameElement):
    IMAGE = "DoorOpen"
    SOLID = False

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    KEY = 1

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %r items! Your inventory is %r" % (len(player.inventory), player.inventory))

class Block(GameElement):
    IMAGE = "Block"
    SOLID = False
    PUSH = True

# Create blocks that you can push
    def interact(self, player):
        GAME_BOARD.set_el(player.x, player.y, PLAYER)

# make sure there's nothing solid in the next item
# check the direction player is going and push 1 over (x or y +1)

####   End class definitions    ####


####   Functions go here    ####

# defin function that recognizes key strokes and assigns direction so Character class method can assign new coordinates  below 
# put this function outside of initialize() because gets called separately in engine.py
def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        GAME_BOARD.draw_msg("You pressed up")
        direction = "up"
        # next_y = PLAYER.y - 1
        # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        # GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.DOWN]:
        GAME_BOARD.draw_msg("You pressed down")
        direction = "down"
        # next_y = PLAYER.y + 1
        # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        # GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)
    elif KEYBOARD[key.LEFT]:
        GAME_BOARD.draw_msg("You pressed left")
        direction = "left"
        # next_x = PLAYER.x - 1
        # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        # GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    elif KEYBOARD[key.RIGHT]:
        GAME_BOARD.draw_msg("You pressed right")
        direction = "right"
        # next_x = PLAYER.x + 1
        # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
        # GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()


    # determines next location coordinates based on key strokes above using Character class method next_pos   
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        # Step 1: Check if player trying to step out of bounds
        if not check_bounds2(next_x, next_y):
            GAME_BOARD.draw_msg("You cannot walk off the board")
        else: 
        # Step 2: Checks if item is there, if so, interact with player
            existing_el = GAME_BOARD.get_el(next_x, next_y)
            if existing_el:
                existing_el.interact(PLAYER)
            
            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
            elif existing_el.SOLID and not hasattr(existing_el, 'LOCKED') and not type('character'):
                 GAME_BOARD.draw_msg("You cannot walk through a solid object")
            elif existing_el.PUSH:
                if direction == "right":
                    GAME_BOARD.set_el(next_x+1, next_y, Block) 

                # GAME_BOARD.set_el(next_x, next_y, PLAYER)

            # If item is a block, delete it and put it in the in the next_x, next y position



# Creates function that checks if moving object within boundaries of board
def check_bounds2(x, y):
    if (0 <= x < GAME_WIDTH) and (0 <= y < GAME_HEIGHT):
        return True
    else: 
        return False


####   Functions end here    ####


# TODO why does this statement below cause infinite printing. If put in if statement, only does once in ending position
    # print "Player positions is here:", (PLAYER.x, PLAYER.y)
    

def initialize():
    """Put game initialization code here"""

    #Initialize and register rock 2
    rock2 = Rock()
    GAME_BOARD.register(rock2)
    GAME_BOARD.set_el(4,4, rock2)

    #Initialize, register, and set on board rock 2
    rock_position = [(2,1), (1,2), (3,2), (2,3)]
    rocks = []

    for pos in rock_position:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # for rock in rocks:
    #     print rock    
    # print "The rock1 is at", (rock1.x, rock1.y)
    # print "The rock2 is at", (rock2.x, rock2.y)
    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE

    # Overrides the SOLID attribute of the last rock in the rocks list
    rocks[-1].SOLID = False    

    # Initialize first player as global variable because will interact with other parts of game
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    NPC = SubCharacter()
    GAME_BOARD.register(NPC)
    GAME_BOARD.set_el(5, 5, NPC)

    # Prints message to the game window
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # initialize, registers and sets the additional items to board
    
    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(8,9,door)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(9,8,wall)

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(8,8,gem)

    key1 = Key()
    GAME_BOARD.register(key1)
    GAME_BOARD.set_el(3,1,key1)

    key2 = Key()
    GAME_BOARD.register(key2)
    GAME_BOARD.set_el(6,3,key2)
    key2.KEY = 2

    
    block = Block()
    GAME_BOARD.register(block)
    GAME_BOARD.set_el(6,6,block)

    # Initialize, register, and sets more walls on board
    wall_position = [(8,7), (7,8)]
    walls = []

    for pos in wall_position:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)

