import sys
import os
import pygame
from pygame.locals import *

class Renderer():
    def __init__(self,
                 dt= 0.1,
                 resolution=(400,450)):
        pygame.init()

        self.dt = dt
        self.resolution = resolution

        self.display = pygame.display.set_mode(self.resolution)
        self.objects = []
        self.clock = pygame.time.Clock()

        self.run()

    def _update_display(self):
        self.display.fill((0,0,0))
        for obj in self.objects:
            obj.sim()
            obj.show()
        
        pygame.display.update()


    def run(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            self._update_display()
            self.clock.tick(float(1 / self.dt))
            

