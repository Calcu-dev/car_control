from abc import ABC
import numpy as np
import pygame

class Vehicle(ABC, pygame.sprite.Sprite):
    def __init__(self):
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center = (200, 200))
        pass

    def _update(self):
        pass
    
    def sim(self, u):
        """Simulate the controls of the input control vector u based on your parameters

        Args:
            u (np.ndarray): Control vector
        """
        pass

    def get_state(self):
        """Obtain the state of the vehicle
        """
        pass


class AckermannSteer(Vehicle):
    def __init__(self,
                 mu = 0,
                 wheel_base = 0,
                 accel_max = 0,
                 ):
        # Friction coefficient
        self.mu = mu
        self.wheel_base = wheel_base
        self.accel_max = accel_max
        self.deccel_max = -accel_max

    def sim(self, u: np.ndarray):
        """Simulate the controls of the input control vector u based on your parameters

        Args:
            u (np.ndarray): Control vector
        """
        pass

    def get_state(self) -> np.ndarray:
        """Obtain the state of the vehicle
        """
        pass

class Test(Vehicle):
    """Test vehicle for demonstration of showing vehicle

    Args:
        Vehicle (Base Class): Base Vehicle Class
    """
    def __init__(self):
        super().__init__()
        self.state = [self.rect.centerx, self.rect.centery]

    def _update(self):
        state = self.get_state()
        self.rect.midbottom = pygame.math.Vector2(state[0], state[1])

    def sim(self, u):
        self.state[0] += u[3] - u[2]
        self.state[1] += u[1] - u[0]

        self._update()
        return self.get_state()

    def get_state(self):
        return self.state
    
    def convert_to_control(self, keys):
        return [k*10 for k in keys]

