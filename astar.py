# Import a library of functions called 'pygame'
import pygame
import graph as graphs
import drawablenode
from drawablenode import *
from math import pi

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PAD = (5, 5)
ROWS = 10
COLS = 10
WIDTH = 50
HEIGHT = 50
SCREEN_WIDTH = COLS * (PAD[0] + WIDTH) + PAD[1]
SCREEN_HEIGHT = ROWS * (PAD[0] + HEIGHT) + PAD[1]

# Set the height and width of the SCREEN
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the nodes
NODES = {}
for i in range(ROWS):
    for j in range(COLS):
        NODES[str([i,j])] = DrawableNode([i,j])

# Add adjacents to each node
for n in NODES:
    # Right
    if str([NODES[n].posx + 1,NODES[n].posy]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx + 1,NODES[n].posy])])
    # Up-Right
    if str([NODES[n].posx + 1,NODES[n].posy + 1]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx + 1,NODES[n].posy + 1])])
    # Up
    if str([NODES[n].posx, NODES[n].posy + 1]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx, NODES[n].posy + 1])])
    # Up-Left
    if str([NODES[n].posx - 1,NODES[n].posy + 1]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx - 1,NODES[n].posy + 1])])
    # Left
    if str([NODES[n].posx - 1,NODES[n].posy]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx - 1,NODES[n].posy])])
    # Down-Left
    if str([NODES[n].posx - 1,NODES[n].posy - 1]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx - 1,NODES[n].posy - 1])])
    # Down
    if str([NODES[n].posx,NODES[n].posy - 1]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx,NODES[n].posy - 1])])
    # Down-Right
    if str([NODES[n].posx + 1,NODES[n].posy - 1]) in NODES:
        NODES[n].adjacents.append(NODES[str([NODES[n].posx + 1,NODES[n].posy - 1])])


NODES[str([3,3])].walkable = False
NODES[str([4,3])].walkable = False
NODES[str([5,2])].walkable = False
NODES[str([5,3])].walkable = False
NODES[str([5,1])].walkable = False
NODES[str([5,0])].walkable = False
NODES[str([4,2])].walkable = False
#NODES[str([1,3])].walkable = False

# Window description
pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
DONE = False
CLOCK = pygame.time.Clock()

pygame.font.init()
font1 = pygame.font.Font(None, 14)
font2 = pygame.font.Font(None, 28)

#set the destination and start point here
start = NODES["[1, 1]"]
dest = NODES["[5, 7]"]


def astar(startnode, destnode):
    opnlist = []
    clslist = []
    current = startnode
    firstchoice = None
    secondchoice = None

    finished = False

    while finished == False:
        opnlist.append(current)
        if current != destnode:
            #Go through adjacents and calculate G, H, F
            for adj in current.adjacents:
                if adj not in clslist and adj.walkable == True:
                    adj.parent = current
                    adj.g = 1
                    adj.h = abs((destnode.posx - adj.posx)) + abs((destnode.posy - adj.posy))
                    adj.f = adj.h + adj.g
                    opnlist.append(adj)
            
            clslist.append(current)
            opnlist.remove(current)

            if opnlist:
                # Sort open list by value of f
                opnlist.sort(key=lambda n: n.f)
                #set current as first in list
                current = opnlist[0]
                # Get rid of the other nodes in the open list and put them in the closed list
                for rest in opnlist:
                    if rest != current:
                        opnlist.remove(rest)
                        clslist.append(rest)
            else:
                current.parent = current
        else:
            finished = True

# Stop

while not DONE:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    CLOCK.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            DONE = True  # Flag that we are DONE so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while DONE==False loop.

    # Clear the SCREEN and set the SCREEN background
    SCREEN.fill(WHITE)

    # Do the A-Star thing
    astar(start,dest)

    # Draw the nodes and connecting lines
    for o in NODES:
        NODES[o].draw(SCREEN, font1)
    
    # Draw guess lines
    for o in NODES:
        if NODES[o].parent:
            pygame.draw.line(SCREEN, RED, (NODES[o].screenpos[0] + 25, NODES[o].screenpos[1] + 25), (NODES[o].parent.screenpos[0] + 25, NODES[o].parent.screenpos[1] + 25), 4)
    
    # Draw quickest path lines
    if dest.parent:
        currn = dest
        while currn != start:
            pygame.draw.line(SCREEN, GREEN, (currn.screenpos[0] + 25, currn.screenpos[1] + 25), (currn.parent.screenpos[0] + 25, currn.parent.screenpos[1] + 25), 6)
            currn = currn.parent

    # Draw the start and destinations as circles
    pygame.draw.circle(SCREEN, BLUE, (start.screenpos[0] + 25, start.screenpos[1] + 25), 10)
    pygame.draw.circle(SCREEN, WHITE, (dest.screenpos[0] + 25, dest.screenpos[1] + 25), 10)

    # Go ahead and update the SCREEN with what we've drawn.
    # This MUST happen after all the other drawing commands.
    bg = pygame.Surface((SCREEN.get_size()[0] / 3, SCREEN.get_size()[1] / 3))
    bg.fill(BLACK)
    textrect = bg.get_rect()
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()