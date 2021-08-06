import numpy as np

from object3d.object3d import Object3D

class Sphere(Object3D):
    def __init__(self, r, center=[0,0,0], resolution=100):
        super().__init__(center, resolution)
        self.r = r
        self.max = self.r + np.linalg.norm(center)

    def getPoint(self, theta, phi):
        x = self.r * np.cos(theta) * np.cos(phi) + self.center[0]
        y = self.r * np.sin(theta) * np.cos(phi) + self.center[1]
        z = self.r * np.sin(phi) + self.center[2]
        return np.array([x, y, z])

    def getPoints(self):
        linspace = np.linspace(0, 2*np.pi, self.resolution, endpoint=False)
        vectors = [
            self.getPoint(theta, phi) \
                for theta in linspace \
                for phi in linspace
        ]
        return np.array(vectors) / self.max

    def getNormalVector(self, theta, phi):
        x = np.cos(theta) * np.cos(phi)
        y = np.sin(theta) * np.cos(phi)
        z = np.sin(phi)
        return np.array([x, y, z])

    def getNormalVectors(self):
        linspace = np.linspace(0, 2*np.pi, self.resolution, endpoint=False)
        vectors = [
            self.getNormalVector(theta, phi) \
                for theta in linspace \
                for phi in linspace
        ]
        return np.array(vectors)