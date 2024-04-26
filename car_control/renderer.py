import sys
import os
import pygame
from vehicles.ackermann import Vehicle, Test, AckermannSteer
from environments.road import RoadRam
from pygame.locals import *

RESOLUTION = (400,400)

class Renderer():
    def __init__(self,
                 environment = None,
                 vehicle : Vehicle = None,
                 dt= 0.1):
        
        if environment is None or vehicle is None:
            raise Exception("Environment or vehicle is not defined!")
        
        pygame.init()

        self.dt = dt
        self.fps = float(1 / self.dt)
        self.resolution = RESOLUTION

        self.display = pygame.display.set_mode(self.resolution)
        self.environment = environment
        self.vehicle = vehicle

        self.reward = 0
        self.max_reward = 100.0

        self.clock = pygame.time.Clock()


    def _draw_vehicle(self, vehicle_state):
        pygame.draw.rect()

    def _update_display(self):
        self.display.fill((0,0,0))
        # Draw things here!

        self.display.blit(self.vehicle.surf, self.vehicle.rect)

        for entity in self.environment.get_sprites():
            self.display.blit(entity.surf, entity.rect)

        pygame.display.update()


    def run(self):
        while True:
            events = pygame.event.get()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            subset_controls = [keys[K_UP], keys[K_DOWN], keys[K_LEFT], keys[K_RIGHT]]
            u = self.vehicle.convert_to_control(subset_controls)

            state = self.vehicle.sim(u)
            self.reward = self.vehicle.distance_traveled / 100.0

            if self.reward > self.max_reward:
                return self.reward
            
            self.environment.update_state(state, self.reward)

            # Check for environment - vehicle collision
            if self.environment.check_vehicle_collision(self.vehicle.rect):
                return self.reward
            
            self._update_display()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    vehicle = AckermannSteer()
    environment=RoadRam(vehicle)
    renderer = Renderer(environment=environment, 
                        vehicle=vehicle)
    
    reward = renderer.run()
    print(reward)

            

