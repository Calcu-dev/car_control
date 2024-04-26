from abc import ABC, abstractmethod
import pygame
import numpy as np
import random
import copy

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(10, 40), random.randint(10, 20)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (random.randint(400, 400), random.randint(-40, -20)))

class Environment(ABC):
    def __init__(self):
        self.sprites = pygame.sprite.Group()

    @abstractmethod
    def _add_obstacle(self):
        pass

    @abstractmethod
    def _collides(self):
        pass

    @abstractmethod
    def _update_display(self, vehicle):
        pass

    def get_sprites(self):
        return self.sprites

    def check_collisions(self, vehicle):
        return self._check_collisions(vehicle)
    
    def get_state(self, vehicle):
        self._update_display(vehicle)

    

class RoadRam(Environment):
    def __init__(self, vehicle):
        super().__init__()
        
        if vehicle is None:
            raise Exception("Vehicle is needed for environment!")

        self.vehicle_state = None
        self.last_vehicle_state = None
        self.vehicle_dimensions = (vehicle.surf.get_width(), vehicle.surf.get_height())
        self._create_random_offscreen()

    def set_environment_bounds(self, bounds):
        self.environment_bounds = pygame.Surface((200, 200))

    def _deriv_state(self):
        if self.last_vehicle_state is None:
            return [0 for x in self.vehicle_state]
        return [x - y for x,y in zip(self.vehicle_state, self.last_vehicle_state)]

    def _add_obstacle(self):
        pass

    def _collides(self, obj, surf):
        return pygame.sprite.collide_rect(obj, surf)
    
    def _create_random_offscreen(self):
        self.sprites.add(Obstacle())

    def _update_display(self):
        if self.vehicle_state is None:
            raise Exception("Vehicle state is not initialized")
        
        d = self._deriv_state()
        print(d)

        for entity in self.sprites:
            entity.rect.y = entity.rect.y - d[1]
            print(entity.rect.y)

        return

    def _get_inbounds(self):
        """Return all objects "in bounds" to the "environment pane"
        """

        pass

    def update_state(self, vehicle_state):
        print("STATE", vehicle_state)
        print("LAST STATE", self.last_vehicle_state)
        if vehicle_state != self.last_vehicle_state:
            self.last_vehicle_state = copy.deepcopy(self.vehicle_state)
            self.vehicle_state = copy.deepcopy(vehicle_state)

        self._update_display()

