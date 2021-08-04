import numpy as np

from object3d.object3d import Object3D

class Cylinder(Object3D):
    def __init__(self, r, H, center=[0,0,0], density=100):
        super().__init__(center, density)
        self.r = r
        self.H = H
        self.max = np.linalg.norm(center) + np.linalg.norm([self.r + self.H/2])

    def getPoint(self, theta, h):
        x = self.r * np.cos(theta) + self.center[0]
        y = self.r * np.sin(theta) + self.center[1]
        z = h + self.center[2]
        return np.array([x, y, z])

    def getPoints(self):
        theta_linspace = np.linspace(0, 2*np.pi, self.density, endpoint=False)
        h_linspace = np.linspace((-1)*self.H/2, self.H/2, self.density)
        vectors = [
            self.getPoint(theta, h) \
                for theta in theta_linspace \
                for h in h_linspace
        ]
        return np.array(vectors) / self.max

    def getNormalVector(self, theta, h):
        x = np.cos(theta)
        y = np.sin(theta)
        z = 0
        return np.array([x, y, z])

    def getNormalVectors(self):
        theta_linspace = np.linspace(0, 2*np.pi, self.density, endpoint=False)
        h_linspace = np.linspace((-1)*self.H/2, self.H/2, self.density)
        vectors = [
            self.getNormalVector(theta, h) \
                for theta in theta_linspace \
                for h in h_linspace
        ]
        return np.array(vectors)