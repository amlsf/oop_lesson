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
class Rock(GameElement):
    IMAGE = "Rock"

# Creates Player Character ot interact with, only instantiated once (not Non-Player Characters)
class Character(GameElement):
    IMAGE = "Horns"

####   End class definitions    ####



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

    rock_position = [(2,1), (1,2), (3,2), (2,3), (3,4)]

    rocks = []

    for pos in rock_position:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock    

    print "The rock1 is at", (rock1.x, rock1.y)
    print "The rock2 is at", (rock2.x, rock2.y)
    print "Rock 1 image", rock1.IMAGE
    print "Rock 2 image", rock2.IMAGE

    # Initialize first player as global variable because
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER