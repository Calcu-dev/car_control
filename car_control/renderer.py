import sys
import os
import pygame
from vehicles.ackermann import Vehicle, Test, AckermannSteer
from environments.road import RoadRam
from pygame.locals import *

import numpy as np
import cv2
import copy

RESOLUTION = (400,800)
DT = 0.05

class Renderer():
    def __init__(self,
                 environment = None,
                 vehicle : Vehicle = None,
                 dt= 0.01,
                 headless=False):
        
        if environment is None or vehicle is None:
            raise Exception("Environment or vehicle is not defined!")
        
        if headless:
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            self.display = pygame.display.set_mode(RESOLUTION)
        else:
            pygame.init()
            self.display = pygame.display.set_mode(RESOLUTION)

        self.headless = headless
        self.dt = dt
        self.fps = float(1 / self.dt)
        self.resolution = RESOLUTION

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


    def step(self, u):
        state = self.vehicle.sim(u)
        self.reward = self.vehicle.distance_traveled / 100.0
        # print(self.reward)

        if self.reward > self.max_reward:
            return self.reward, True
        
        self.environment.update_state(state, self.reward)
        self._update_display()

        # Check for environment - vehicle collision
        if self.environment.check_vehicle_collision(self.vehicle.rect):
            return self.reward, True
        
        return self.reward, False
    
    def run_test(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            obs = np.uint8(copy.deepcopy(pygame.surfarray.pixels3d(self.display)))
            # cv2.imshow("window", cv2.rotate(obs, cv2.ROTATE_90_CLOCKWISE))
            # cv2.waitKey(1)
            
            subset_controls = [1, 0, 0, 0]
            u = self.vehicle.convert_to_control(subset_controls)

            reward, done = self.step(u)
            if done:
                return reward
            
            self.clock.tick(self.fps)


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

            reward, done = self.step(u)
            if done:
                return reward
            
            self.clock.tick(self.fps)


if __name__ == "__main__":
    vehicle = AckermannSteer(dt=DT, resolution=RESOLUTION)
    environment=RoadRam(vehicle, RESOLUTION, DT)
    renderer = Renderer(environment=environment, 
                        vehicle=vehicle,
                        dt=DT,
                        headless=True)
    
    reward = renderer.run_test()
    print(reward)

            

