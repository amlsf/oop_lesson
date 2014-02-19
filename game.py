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

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####

# Creates rock instances of Rock class
# TODO is Rock a subclass of Subelement that inherits all its properties? 
class Rock(GameElement):
    # Pulls image nicknamed Rock from setup_images function in engine.py
    IMAGE = "Rock"
    # creates solid attribute so don't have to check if various elements for walking through
    SOLID = True

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

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" %(player.inventory, len(player.inventory)))

####   End class definitions    ####


# put outside of initialize() because gets called separately in engine.py
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


### TODO check bounds probably goes here somewhere, why doesn't check_bounds() print message when walk off board, as part of get_el, set_el, del_el
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        #Checks what is in the next position
        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(PLAYER)
# This print statement prints any time interact with something, need some sort of if stmt
            # print "Your current inventory is: ", PLAYER.inventory

        # If there's nothing there _or_ if the existing element is not solid, walk through
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
        else:
            GAME_BOARD.draw_msg("You cannot walk through a solid object")


# TODO why does this statement below cause infinite printing. If put in if statement, only does once in ending position
    # print "Player positions is here:", (PLAYER.x, PLAYER.y)
    

def initialize():
    """Put game initialization code here"""

    #Initialize and register rock 1
    rock1 = Rock()
    GAME_BOARD.register(rock1)
    GAME_BOARD.set_el(0,0,rock1)

    #Initialize and register rock 2
    rock2 = Rock()
    GAME_BOARD.register(rock2)
    GAME_BOARD.set_el(4,4, rock2)

    #Intialize and register more rocks
    rock_position = [(2,1), (1,2), (3,2), (2,3)]
    rocks = []

    for pos in rock_position:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # Overrides the SOLID attribute of the last rock in the rocks list
    rocks[-1].SOLID = False    

    for rock in rocks:
        print rock    

    print "The rock1 is at", (rock1.x, rock1.y)
    print "The rock2 is at", (rock2.x, rock2.y)
    print "Rock 1 image", rock1.IMAGE
    print "Rock 2 image", rock2.IMAGE

    # Initialize first player as global variable because will interact with other parts of game
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    # Prints to the game window
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3,1,gem)

