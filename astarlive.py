# Import a library of functions called 'pygame'
import pygame
import drawablenode
from drawablenode import *
from math import pi
import random
from constants import *
from gametemp import GameTemplate


class AStarGame(GameTemplate):
    def __init__(self):
        # Initialize the game engine
        pygame.init()

        # Set the height and width of the SCREEN
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Create the nodes
        self.NODES = {}
        for i in range(ROWS):
            for j in range(COLS):
                self.NODES[str([i,j])] = DrawableNode([i,j])

        # Add adjacents to each node
        for n in self.NODES:
            # Right
            if str([self.NODES[n].posx + 1,self.NODES[n].posy]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx + 1,self.NODES[n].posy])])
            # Up-Right
            if str([self.NODES[n].posx + 1,self.NODES[n].posy + 1]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx + 1,self.NODES[n].posy + 1])])
            # Up
            if str([self.NODES[n].posx, self.NODES[n].posy + 1]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx, self.NODES[n].posy + 1])])
            # Up-Left
            if str([self.NODES[n].posx - 1,self.NODES[n].posy + 1]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx - 1,self.NODES[n].posy + 1])])
            # Left
            if str([self.NODES[n].posx - 1,self.NODES[n].posy]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx - 1,self.NODES[n].posy])])
            # Down-Left
            if str([self.NODES[n].posx - 1,self.NODES[n].posy - 1]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx - 1,self.NODES[n].posy - 1])])
            # Down
            if str([self.NODES[n].posx,self.NODES[n].posy - 1]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx,self.NODES[n].posy - 1])])
            # Down-Right
            if str([self.NODES[n].posx + 1,self.NODES[n].posy - 1]) in self.NODES:
                self.NODES[n].adjacents.append(self.NODES[str([self.NODES[n].posx + 1,self.NODES[n].posy - 1])])

        # Window description
        pygame.display.set_caption("Example code for A-Star")

        # Loop until the user clicks the close button.
        self.DONE = False
        self.CLOCK = pygame.time.Clock()

        pygame.font.init()
        self.font1 = pygame.font.Font(None, 14)
        self.font2 = pygame.font.Font(None, 28)

        # Set the destination and self.start point here
        self.start = self.NODES["[0, 0]"]
        self.dest = self.NODES[str([ROWS-1,COLS-1])]
        self.selnode = self.NODES["[0, 0]"]

        self.currentNode = self.start
        self.opnlist = []
        self.clslist = []

        self.currentNode.g = 1
        self.currentNode.h = (abs((self.dest.posx - self.currentNode.posx)) + abs((self.dest.posy - self.currentNode.posy))) * 10
        self.currentNode.f = self.currentNode.h + self.currentNode.g

        self.opnlist.append(self.currentNode)

        self.keepgoing = False

    def _update(self):
        # Leave this out and we will use all CPU we can.
        self.CLOCK.tick(FPS)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.DONE = True  # Flag that we are self.DONE so we exit this loop

        if self.keepgoing == True:
            # Do the A-Star thing if safe
            if self.dest.walkable == True and self.start.walkable == True:
                if self.opnlist and self.currentNode != self.dest:
                    self.currentNode = self.opnlist[0]

                    #Add the current node to the closed list
                    self.opnlist.remove(self.currentNode)
                    self.clslist.append(self.currentNode)
                    #Go through adjacents and calculate G, H, F
                    for adj in self.currentNode.adjacents:
                        if adj not in self.clslist and adj.walkable == True:
                            if adj not in self.opnlist:
                                self.opnlist.append(adj)
                            adj.g = 10 + self.currentNode.g
                            # Manhattan (absolute distance from current node to destination)
                            adj.h = (abs((self.dest.posx - adj.posx)) + abs((self.dest.posy - adj.posy))) * 10
                            adj.f = adj.h + adj.g
                            if adj.parent:
                                if adj.parent.g > self.currentNode.g:
                                    adj.parent = self.currentNode
                            else:
                                adj.parent = self.currentNode

                    # Sort open list by value of f
                    self.opnlist.sort(key=lambda n: n.f)

        # If pressed uparrow, move destination up
        if pygame.key.get_pressed()[pygame.K_UP]:
            if self.selnode.posy > 0: self.selnode = self.NODES[str([self.selnode.posx,self.selnode.posy-1])]
        # If pressed downarrow, move destination down
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.selnode.posy < COLS-1: self.selnode = self.NODES[str([self.selnode.posx,self.selnode.posy+1])]
        # If pressed leftarrow, move destination left
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.selnode.posx > 0: self.selnode = self.NODES[str([self.selnode.posx-1,self.selnode.posy])]
        # If pressed rightarrow, move destination right
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.selnode.posx < ROWS-1: self.selnode = self.NODES[str([self.selnode.posx+1,self.selnode.posy])]
        # If pressed S, set self.start to selected
        if pygame.key.get_pressed()[pygame.K_s]:
            self.start = self.selnode
            self.currentNode = self.start
            self.opnlist = []
            self.clslist = []
            self.opnlist.append(self.currentNode)
                # Reset all node values
            for noodles in self.NODES:
                self.NODES[noodles].parent = None
                self.NODES[noodles].h = 0
                self.NODES[noodles].f = 0
                self.NODES[noodles].g = 0
            self.currentNode.g = 1
            self.currentNode.h = abs((self.dest.posx - self.currentNode.posx)) + abs((self.dest.posy - self.currentNode.posy))
            self.currentNode.f = self.currentNode.h + self.currentNode.g
        # If pressed D, set destination to selected
        if pygame.key.get_pressed()[pygame.K_d]:
            self.dest = self.selnode
            self.start = self.currentNode
            self.opnlist = []
            self.clslist = []
            self.opnlist.append(self.currentNode)
                # Reset all node values
            for noodles in self.NODES:
                self.NODES[noodles].parent = None
                self.NODES[noodles].h = 0
                self.NODES[noodles].f = 0
                self.NODES[noodles].g = 0
            self.currentNode.g = 1
            self.currentNode.h = abs((self.dest.posx - self.currentNode.posx)) + abs((self.dest.posy - self.currentNode.posy))
            self.currentNode.f = self.currentNode.h + self.currentNode.g
        # If pressed A, make selected walkable true/false
        if pygame.key.get_pressed()[pygame.K_a]:
            if self.selnode.walkable == True: self.selnode.walkable = False
            else: self.selnode.walkable = True
        # If pressed C, clear all unwalkable nodes
        if pygame.key.get_pressed()[pygame.K_c]:
            for noodles in self.NODES:
                self.NODES[noodles].walkable = True
        if pygame.key.get_pressed()[pygame.K_x]:
            for noodles in self.NODES:
                if self.NODES[noodles] != self.start and self.NODES[noodles] != self.dest:
                    self.NODES[noodles].walkable = not self.NODES[noodles].walkable
                else:
                    self.NODES[noodles].walkable = True
        if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.keepgoing = not self.keepgoing
        if pygame.key.get_pressed()[pygame.K_z]:
            for noodles in self.NODES:
                self.NODES[noodles].walkable = random.choice([True,False])
            self.start.walkable = True
            self.dest.walkable = True


    def _draw(self):
        # Clear the self.SCREEN and set the self.SCREEN background
        self.SCREEN.fill(DARK)

        # Draw the nodes
        for o in self.NODES:
            self.NODES[o].draw(self.SCREEN, self.font1)

        # Draw the self.start, destination, and selected nodes as circles
        pygame.draw.circle(self.SCREEN, GREEN, (self.start.screenpos[0] + WIDTH/2, self.start.screenpos[1] + HEIGHT/2), 6)
        pygame.draw.circle(self.SCREEN, REDRED, (self.dest.screenpos[0] + WIDTH/2, self.dest.screenpos[1] + HEIGHT/2), 6)
        pygame.draw.circle(self.SCREEN, WHITE, (self.selnode.screenpos[0] + WIDTH/2, self.selnode.screenpos[1] + HEIGHT/2), 6)
        pygame.draw.circle(self.SCREEN, REDRED, (self.currentNode.screenpos[0] + WIDTH/2, self.currentNode.screenpos[1] + HEIGHT/2), 6)

        # Draw guess lines
        if EYECANDY:
            for o in self.NODES:
                if self.NODES[o].parent:
                    pygame.draw.line(self.SCREEN, (random.randrange(100, 255), random.randrange(100, 255), random.randrange(100, 255)), (self.NODES[o].screenpos[0] + WIDTH/2, self.NODES[o].screenpos[1] + HEIGHT/2),
                                    (self.NODES[o].parent.screenpos[0] + WIDTH/2,
                                    self.NODES[o].parent.screenpos[1] + HEIGHT/2), 4)
        else:
            for o in self.NODES:
                if self.NODES[o].parent:
                    pygame.draw.line(self.SCREEN, RED, (self.NODES[o].screenpos[0] + WIDTH/2, self.NODES[o].screenpos[1] + HEIGHT/2),
                                    (self.NODES[o].parent.screenpos[0] + WIDTH/2,
                                    self.NODES[o].parent.screenpos[1] + HEIGHT/2), 4)

        # Draw quickest path lines
        if self.dest.parent:
            currn = self.dest
            while currn != self.start:
                pygame.draw.line(self.SCREEN, GREEN, (currn.screenpos[0] + WIDTH/2, currn.screenpos[1] + HEIGHT/2), (currn.parent.screenpos[0] + WIDTH/2, currn.parent.screenpos[1] + HEIGHT/2), 6)
                currn = currn.parent

        # Go ahead and update the self.SCREEN with what we've drawn.
        # This MUST happen after all the other drawing commands.
        bg = pygame.Surface((self.SCREEN.get_size()[0] / 3, self.SCREEN.get_size()[1] / 3))
        bg.fill(BLACK)
        textrect = bg.get_rect()
        pygame.display.flip()

    def _shutdown(self):
        # Be IDLE friendly
        pygame.quit()

    def _startup(self):
        while self.DONE == False:
            self._update()
            self._draw()
        self._shutdown()