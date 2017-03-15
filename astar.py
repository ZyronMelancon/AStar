# Import a library of functions called 'pygame'
import pygame
import graph as graphs
from graph import Graph
from graph import Node
import drawablenode
from drawablenode import *

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
search_space = Graph([ROWS, COLS])

# Create the nodes
NODES = []
for i in range(ROWS):
    for j in range(COLS):
        node = search_space.get_node([i, j])
        NODES.append(DrawableNode(node))

# Add adjacents
for i in NODES:
    if search_space.get_node([i.x + 1, i.y]):
        node = search_space.get_node([i.x + 1, i.y])
        i.adjacents.append(node)
    if search_space.get_node([i.x - 1, i.y]):
        node = search_space.get_node([i.x - 1, i.y])
        i.adjacents.append(node)
    if search_space.get_node([i.x, i.y + 1]):
        node = search_space.get_node([i.x, i.y + 1])
        i.adjacents.append(node)
    if search_space.get_node([i.x, i.y - 1]):
        node = search_space.get_node([i.x, i.y - 1])
        i.adjacents.append(node)

# Window description
pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
DONE = False
CLOCK = pygame.time.Clock()

pygame.font.init()
font1 = pygame.font.Font(None, 14)
font2 = pygame.font.Font(None, 28)

#set the destination and start point here
start = NODES[4]
dest = NODES[15]


def astar(startnode, destnode):
    opnlist = []
    clslist = []
    current = startnode
    opnlist.append(current)

    while opnlist:
        if current != destnode:
            #Go through adjacents and calculate G, H, F
            for adj in current.adjacents:
                if adj not in clslist:
                    adj.parent = current
                    adj.g = 1
                    adj.h = abs((destnode.x - adj.x)) + abs((destnode.y - adj.y))
                    adj.f = adj.h + adj.g
                    opnlist.append(adj)

            clslist.append(current)
            opnlist.remove(current)
            # Sort open list by value of f
            opnlist.sort(key=lambda n: n.f)
            #set current as first in list
            current = opnlist[0]
            # Get rid of the other nodes in the open list and put them in the closed list
            for rest in opnlist:
                if rest != current:
                    opnlist.remove(rest)
                    clslist.append(rest)

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

    # Draw the nodes
    for i in NODES:
        i.draw(SCREEN, font1)

    # Go ahead and update the SCREEN with what we've drawn.
    # This MUST happen after all the other drawing commands.
    bg = pygame.Surface((SCREEN.get_size()[0] / 3, SCREEN.get_size()[1] / 3))
    bg.fill(BLACK)
    textrect = bg.get_rect()
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()