import pygame
from constants import *

class GameTemplate(object):
    def __init__(self):
        pygame.init()
        
    def _startup(self):
        return True

    def _update(self):
        return True

    def _draw(self):
        '''draw'''

    def _shutdown(self):
        '''shutdown'''