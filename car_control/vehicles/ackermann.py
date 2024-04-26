from abc import ABC
import numpy as np
import pygame

class Vehicle(ABC, pygame.sprite.Sprite):
    def __init__(self, resolution, dt):
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (int(resolution[0]/2), int(resolution[1]/2)))

        self.dt = dt
        self.distance_traveled = 0
        pass

    def _update(self):
        state = self.get_state()
        self.rect.midbottom = pygame.math.Vector2(state[0], state[1])
        self.distance_traveled += self.state[2] * self.dt
    
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
                 mu = 0.2,
                 wheel_base = .48,
                 accel_max = 100,
                 vel_max = 200,
                 steer_max = 45.0,
                 steer_rate = 4,
                 dt = 0.1,
                 resolution = (400,400)
                 ):
        super().__init__(resolution=resolution, dt=dt)
        self.mu = mu
        self.wheel_base = wheel_base
        self.accel_max = accel_max
        self.deccel_max = -accel_max
        self.vel_max = vel_max 
        self.steer_max = steer_max
        self.steer_rate = steer_rate
        self.dt = dt
        self.state = [self.rect.centerx, self.rect.centery, 0, 0]
        

    def sim(self, u: np.ndarray):
        """Simulate the controls of the input control vector u based on your parameters

        Args:
            state (np.ndarray):         Input vehicle state - [x, y, v, yaw]
            u (np.ndarray):             Control vector - [accel_effort [0 -> 1], steering_effort[0 -> 1]]
        """
        
        """ Computing change in states """

        prior_vel = self.state[2]

        delta_v = self.accel_max * u[0] * self.dt
        delta_angle = self.steer_rate * u[1]  * self.dt 
        
        vel_update = prior_vel + delta_v# - self.mu * self.dt
        delta_angle = np.clip(delta_angle, -1 * self.steer_max, self.steer_max)
        angle_update = delta_angle
        
        vel_update = np.clip(vel_update, 0, self.vel_max)
        
        # self.state[1] -= vel_update * np.cos(angle_update) * self.dt                         # x position update
        # self.state[0] -= vel_update * np.sin(angle_update) * self.dt                         # y position update
        self.state[2] = vel_update                                                        # velocity update
        self.state[3] += (vel_update * np.tan(angle_update)) / self.wheel_base * self.dt     # yaw update
        self.state[3] = np.clip(self.state[3], -self.steer_max, self.steer_max)
        
        self._update()
        return self.get_state()    

    def get_state(self) -> np.ndarray:
        """Obtain the state of the vehicle
        """
        """ Single step rollout"""

        return self.state 
    
    def convert_to_control(self, u):
        return [u[0] - u[1], u[2] - u[3]]
        

class Test(Vehicle):
    """Test vehicle for demonstration of showing vehicle

    Args:
        Vehicle (Base Class): Base Vehicle Class
    """
    def __init__(self):
        super().__init__()
        self.state = [self.rect.centerx, self.rect.centery]

    def sim(self, u):
        self.state[0] += u[3] - u[2]
        self.state[1] += u[1] - u[0]

        self._update()
        return self.get_state()

    def get_state(self):
        return self.state
    
    def convert_to_control(self, keys):
        return [k*10 for k in keys]

