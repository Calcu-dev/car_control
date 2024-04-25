from abc import ABC
import numpy as np

class Vehicle(ABC):
    def __init__(self):
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
        pass

    def sim(self):
        pass

    def get_state(self):
        pass

