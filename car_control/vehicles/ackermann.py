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
                 mu = 7,
                 wheel_base = .48,
                 accel_max = 2,
                 vel_max = 25,
                 steer_max = np.pi/6,
                 steer_rate = 4,
                 dt = 0.01,
                 ):
        self.mu = mu
        self.wheel_base = wheel_base
        self.accel_max = accel_max
        self.deccel_max = -accel_max
        self.vel_max = vel_max 
        self.steer_max = steer_max
        self.steer_rate = steer_rate
        self.dt = dt
        

    def sim(self, u: np.ndarray, prior_vel, prior_yaw):
        """Simulate the controls of the input control vector u based on your parameters

        Args:
            state (np.ndarray):         Input vehicle state - [x, y, v, yaw]
            u (np.ndarray):             Control vector - [accel_effort [0 -> 1], steering_effort[0 -> 1]]
        """
        
        """ Computing change in states """
        delta_v = self.accel_max * u[0] * self.dt
        delta_angle = self.steer_rate * u[1]  * self.dt 
        
        vel_update = prior_vel + delta_v
        angle_update = prior_yaw + delta_angle
        
        vel_update = np.clip(vel_update, 0, self.vel_max)
        angle_update = np.clip(angle_update, -1 * self.steer_max, self.steer_max)
        
        return vel_update, angle_update    

    def get_state(self, u: np.ndarray, state: np.ndarray) -> np.ndarray:
        """Obtain the state of the vehicle
        """
        """ Single step rollout"""
        new_v, new_theta = self.sim(u, state[2], state[3])
        
        state[0] += new_v * np.cos(new_theta) * self.dt                         # x position update
        state[1] += new_v * np.sin(new_theta) * self.dt                         # y position update
        state[2] = new_v                                                        # velocity update
        state[3] += (new_v * np.tan(new_theta)) / self.wheel_base * self.dt     # yaw update
        
        return state 

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

