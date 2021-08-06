import numpy as np

from object3d.object3d import Object3D

class Torus(Object3D):
    def __init__(self, R, r, center=[0,0,0], resolution=100):
        # https://web.cs.ucdavis.edu/~amenta/s12/findnorm.pdf
        super().__init__(center, resolution)
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
        x = (self.r_b+self.r_l*np.cos(theta))*np.cos(phi) + self.center[0]
        y = (self.r_b+self.r_l*np.cos(theta))*np.sin(phi) + self.center[1]
        z = self.r_l * np.sin(theta) + self.center[2]
        return np.array([x, y, z])

    def getPoints(self):
        """
        Get all points defined by grided theta and phi
        """
        linspace = np.linspace(0, 2*np.pi, self.resolution)
        vectors = [
            self.getPoint(theta, phi) \
                for theta in linspace \
                for phi in linspace \
        ]
        return np.array(vectors) / self.max

    def getNormalVector(self, theta, phi):
        # https://trecs.se/torus.php
        x = np.cos(theta) * np.cos(phi)
        y = np.cos(theta) * np.sin(phi)
        z = np.sin(theta)
        return np.array([x, y, z])

    def getNormalVectors(self):
        linspace = np.linspace(0, 2*np.pi, self.resolution)
        vectors = [
            self.getNormalVector(theta, phi) \
                for theta in linspace \
                for phi in linspace \
        ]
        return np.array(vectors)


