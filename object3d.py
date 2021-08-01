from abc import ABCMeta, abstractmethod
import math

import numpy as np

class Object3D(metaclass=ABCMeta):
    def __init__(self, center:list, density:int):
        self.center = center
        self.density = density

    def __call__(self, *args):
        points = self.getPoints(*args)
        norms = self.getNormalVectors(*args)
        return points, norms

    @abstractmethod
    def getPoint(self, *args):
        pass

    @abstractmethod
    def getPoints(self, *args):
        pass

    @abstractmethod
    def getNormalVector(self, *args):
        pass

    @abstractmethod
    def getNormalVectors(self, *args):
        pass

class Torus(Object3D):
    def __init__(self, R, r, center=[0,0,0], density=100):
        # https://web.cs.ucdavis.edu/~amenta/s12/findnorm.pdf
        super().__init__(center, density)
        self.r_b = R      ## The torus center to the tube center
        self.r_l = r      ## The radius of the tube
        self.max = R + r + np.linalg.norm(center)

    def getPoint(self, theta, phi):
        """
        Get a single point defined by theta and phi
        Args :
            theta : angle from the tube center to the tube surface
            phi : Angle from the torus center to the tube center
        """
        x = (self.r_b+self.r_l*math.cos(theta))*math.cos(phi) + self.center[0]
        y = (self.r_b+self.r_l*math.cos(theta))*math.sin(phi) + self.center[1]
        z = self.r_l * math.sin(theta) + self.center[2]
        return np.array([x, y, z])

    def getPoints(self):
        """
        Get all points defined by grided theta and phi
        """
        linspace = np.linspace(0, 2*math.pi, self.density)
        vectors = [
            self.getPoint(theta, phi) \
                for theta in linspace \
                for phi in linspace \
        ]
        return np.array(vectors) / self.max

    def getNormalVector(self, theta, phi):
        # https://trecs.se/torus.php
        x = math.cos(theta) * math.cos(phi)
        y = math.cos(theta) * math.sin(phi)
        z = math.sin(theta)
        return np.array([x, y, z])

    def getNormalVectors(self):
        linspace = np.linspace(0, 2*math.pi, self.density)
        vectors = [
            self.getNormalVector(theta, phi) \
                for theta in linspace \
                for phi in linspace \
        ]
        return np.array(vectors)

