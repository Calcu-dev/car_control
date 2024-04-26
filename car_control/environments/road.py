from abc import ABC, abstractmethod
import pygame
import numpy as np
import random
import copy

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, size = None, coords = None):
        super().__init__()
        size = size if size is not None else (random.randint(10, 100), random.randint(10, 20))
        coords = coords if coords is not None else (random.randint(0, 400), random.randint(-40, -20))

        self.surf = pygame.Surface(size)
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = coords)

class Environment(ABC):
    def __init__(self, resolution, dt):
        self.sprites = pygame.sprite.Group()

        self.delete_surface = Obstacle(size=(resolution[0]*10, 1), coords=(int(resolution[0]/2), resolution[1]))
        self.max_objs = 10
        self.last_reward_since_obs = 0
        self.dt = dt

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
    def __init__(self, vehicle, resolution, dt):
        super().__init__(resolution, dt)
        
        if vehicle is None:
            raise Exception("Vehicle is needed for environment!")

        self.vehicle_state = None
        self.last_vehicle_state = None
        self.vehicle_dimensions = (vehicle.surf.get_width(), vehicle.surf.get_height())
        self._create_random_offscreen()

    def _deriv_state(self):
        if self.last_vehicle_state is None:
            return [0 for x in self.vehicle_state]
        return [x - y for x,y in zip(self.vehicle_state, self.last_vehicle_state)]

    def _add_obstacle(self):
        self.sprites.add(Obstacle())

    def _collides(self, obj, surf):

        if type(obj) == pygame.sprite.Sprite and type(surf) == pygame.sprite.Sprite:
            return pygame.sprite.collide_rect(obj, surf)
        
        if type(obj) == Obstacle:
            obj = obj.rect

        if type(surf) == Obstacle:
            surf = surf.rect

        return surf.colliderect(obj)
    
    def check_vehicle_collision(self, vehicle):
        for entity in self.sprites:
            if self._collides(entity, vehicle):
                return True
            
        return False
    
    def _create_random_offscreen(self):
        self.sprites.add(Obstacle())

    def _update_display(self):
        if self.vehicle_state is None:
            raise Exception("Vehicle state is not initialized")
        
        delete_list = []
        for entity in self.sprites:
            delete_list.append(entity if self._collides(entity, self.delete_surface) else None)

            entity.rect.y = entity.rect.y + np.cos(np.deg2rad(self.vehicle_state[3])) * self.vehicle_state[2] * self.dt
            entity.rect.x = entity.rect.x + np.sin(np.deg2rad(self.vehicle_state[3])) * self.vehicle_state[2] * self.dt
        
        # Remove entities
        for entity in delete_list:
            if entity is None:
                continue
            self.sprites.remove(entity)  

        return

    def _get_inbounds(self):
        """Return all objects "in bounds" to the "environment pane"
        """

        pass

    def update_state(self, vehicle_state, reward):
        if vehicle_state != self.last_vehicle_state:
            self.last_vehicle_state = copy.deepcopy(self.vehicle_state)
            self.vehicle_state = copy.deepcopy(vehicle_state)

        if len(self.sprites) < self.max_objs:
            if random.randint(0, 100) < reward and (reward - self.last_reward_since_obs) > 1 :
                self._add_obstacle()
                self.last_reward_since_obs = reward

        self._update_display()

pass