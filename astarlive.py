# Import a library of functions called 'pygame'
import pygame
import drawablenode
from drawablenode import *
from math import pi
import random

# Initialize the game engine
pygame.init()


# Visual settings
EYECANDY = True
FPS = 15

# Window and Node sizes
PAD = (5, 5)
ROWS = 50
COLS = 25
WIDTH = 30
HEIGHT = 30
SCREEN_WIDTH = ROWS * (PAD[0] + WIDTH) + PAD[1]
SCREEN_HEIGHT = COLS * (PAD[0] + HEIGHT) + PAD[1]

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK = (15, 15, 15)
BLUE = (0, 0, 100)
GREEN = (0, 180, 0)
RED = (100, 0, 100)
REDRED = (255, 0, 0)

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

# Window description
pygame.display.set_caption("Example code for A-Star")

# Loop until the user clicks the close button.
DONE = False
CLOCK = pygame.time.Clock()

pygame.font.init()
font1 = pygame.font.Font(None, 14)
font2 = pygame.font.Font(None, 28)

# Set the destination and start point here
start = NODES["[0, 0]"]
dest = NODES[str([ROWS-1,COLS-1])]
selnode = NODES["[0, 0]"]

currentNode = start
opnlist = []
clslist = []

currentNode.g = 1
currentNode.h = (abs((dest.posx - currentNode.posx)) + abs((dest.posy - currentNode.posy))) * 10
currentNode.f = currentNode.h + currentNode.g

opnlist.append(currentNode)

keepgoing = False

# Stop
while not DONE:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    CLOCK.tick(FPS)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            DONE = True  # Flag that we are DONE so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while DONE==False loop.

    # Clear the SCREEN and set the SCREEN background
    SCREEN.fill(DARK)

    # Draw the nodes
    for o in NODES:
        NODES[o].draw(SCREEN, font1)

    # Draw the start, destination, and selected nodes as circles
    pygame.draw.circle(SCREEN, GREEN, (start.screenpos[0] + WIDTH/2, start.screenpos[1] + HEIGHT/2), 6)
    pygame.draw.circle(SCREEN, REDRED, (dest.screenpos[0] + WIDTH/2, dest.screenpos[1] + HEIGHT/2), 6)
    pygame.draw.circle(SCREEN, WHITE, (selnode.screenpos[0] + WIDTH/2, selnode.screenpos[1] + HEIGHT/2), 6)
    pygame.draw.circle(SCREEN, REDRED, (currentNode.screenpos[0] + WIDTH/2, currentNode.screenpos[1] + HEIGHT/2), 6)

    if keepgoing == True:
        # Do the A-Star thing if safe
        if dest.walkable == True and start.walkable == True:
            if opnlist and currentNode != dest:
                currentNode = opnlist[0]

                #Add the current node to the closed list
                opnlist.remove(currentNode)
                clslist.append(currentNode)
                #Go through adjacents and calculate G, H, F
                for adj in currentNode.adjacents:
                    if adj not in clslist and adj.walkable == True:
                        if adj not in opnlist:
                            opnlist.append(adj)
                        adj.g = 10 + currentNode.g
                        # Manhattan (absolute distance from current node to destination)
                        adj.h = (abs((dest.posx - adj.posx)) + abs((dest.posy - adj.posy))) * 10
                        adj.f = adj.h + adj.g
                        if adj.parent:
                            if adj.parent.g > currentNode.g:
                                adj.parent = currentNode
                        else:
                            adj.parent = currentNode

                # Sort open list by value of f
                opnlist.sort(key=lambda n: n.f)

    # Draw guess lines
    if EYECANDY:
        for o in NODES:
            if NODES[o].parent:
                pygame.draw.line(SCREEN, (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255)), (NODES[o].screenpos[0] + WIDTH/2, NODES[o].screenpos[1] + HEIGHT/2),
                                (NODES[o].parent.screenpos[0] + WIDTH/2,
                                NODES[o].parent.screenpos[1] + HEIGHT/2), 4)
    else:
        for o in NODES:
            if NODES[o].parent:
                pygame.draw.line(SCREEN, RED, (NODES[o].screenpos[0] + WIDTH/2, NODES[o].screenpos[1] + HEIGHT/2),
                                (NODES[o].parent.screenpos[0] + WIDTH/2,
                                NODES[o].parent.screenpos[1] + HEIGHT/2), 4)

    # Draw quickest path lines
    if dest.parent:
        currn = dest
        while currn != start:
            pygame.draw.line(SCREEN, GREEN, (currn.screenpos[0] + WIDTH/2, currn.screenpos[1] + HEIGHT/2), (currn.parent.screenpos[0] + WIDTH/2, currn.parent.screenpos[1] + HEIGHT/2), 6)
            currn = currn.parent

    # If pressed uparrow, move destination up
    if pygame.key.get_pressed()[pygame.K_UP]:
        if selnode.posy > 0: selnode = NODES[str([selnode.posx,selnode.posy-1])]
    # If pressed downarrow, move destination down
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if selnode.posy < COLS-1: selnode = NODES[str([selnode.posx,selnode.posy+1])]
    # If pressed leftarrow, move destination left
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if selnode.posx > 0: selnode = NODES[str([selnode.posx-1,selnode.posy])]
    # If pressed rightarrow, move destination right
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if selnode.posx < ROWS-1: selnode = NODES[str([selnode.posx+1,selnode.posy])]
    # If pressed S, set start to selected
    if pygame.key.get_pressed()[pygame.K_s]:
        start = selnode
        currentNode = start
        opnlist = []
        clslist = []
        opnlist.append(currentNode)
            # Reset all node values
        for noodles in NODES:
            NODES[noodles].parent = None
            NODES[noodles].h = 0
            NODES[noodles].f = 0
            NODES[noodles].g = 0
        currentNode.g = 1
        currentNode.h = abs((dest.posx - currentNode.posx)) + abs((dest.posy - currentNode.posy))
        currentNode.f = currentNode.h + currentNode.g
    # If pressed D, set destination to selected
    if pygame.key.get_pressed()[pygame.K_d]:
        dest = selnode
        start = currentNode
        opnlist = []
        clslist = []
        opnlist.append(currentNode)
            # Reset all node values
        for noodles in NODES:
            NODES[noodles].parent = None
            NODES[noodles].h = 0
            NODES[noodles].f = 0
            NODES[noodles].g = 0
        currentNode.g = 1
        currentNode.h = abs((dest.posx - currentNode.posx)) + abs((dest.posy - currentNode.posy))
        currentNode.f = currentNode.h + currentNode.g
    # If pressed A, make selected walkable true/false
    if pygame.key.get_pressed()[pygame.K_a]:
         if selnode.walkable == True: selnode.walkable = False
         else: selnode.walkable = True
    # If pressed C, clear all unwalkable nodes
    if pygame.key.get_pressed()[pygame.K_c]:
        for noodles in NODES:
            NODES[noodles].walkable = True
    if pygame.key.get_pressed()[pygame.K_x]:
        for noodles in NODES:
            if NODES[noodles] != start and NODES[noodles] != dest:
                NODES[noodles].walkable = not NODES[noodles].walkable
            else:
                NODES[noodles].walkable = True
    if pygame.key.get_pressed()[pygame.K_SPACE]:
            keepgoing = not keepgoing
    if pygame.key.get_pressed()[pygame.K_z]:
        for noodles in NODES:
            NODES[noodles].walkable = random.choice([True,False])
        start.walkable = True
        dest.walkable = True

    # Go ahead and update the SCREEN with what we've drawn.
    # This MUST happen after all the other drawing commands.
    bg = pygame.Surface((SCREEN.get_size()[0] / 3, SCREEN.get_size()[1] / 3))
    bg.fill(BLACK)
    textrect = bg.get_rect()
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()