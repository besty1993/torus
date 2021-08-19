import numpy as np

from object3d.object3d import Object3D

class Cone(Object3D):
    def __init__(self, R, H, center=[0,0,0], resolution=100):
        """
        Define a cone
        Args:
            R: maximum radius of the cone
            H: The height of the cone
            center: The center of the cone; it would be half of the height
            resolution: The resolution of the object points
            max: The maximum possible distance
        """
        super().__init__(center, resolution)
        self.R = R
        self.H = H
        self.max = np.linalg.norm(center) + np.linalg.norm([self.R + self.H/2])

    def getPoint(self, theta, h, r):
        """
        Get point defined by three parameters
        Args:
            theta: degree on x-y plane
            h: the target height
            r: Radius at underside(Used for underside only)
        """
        if h == 0:
            x = r * np.cos(theta) + self.center[0]
            y = r * np.sin(theta) + self.center[1]
            z = (self.H/2) * (-1) + self.center[2]
        else:
            temp_r = (self.H-h) * self.R / self.H
            x = temp_r * np.cos(theta) + self.center[0]
            y = temp_r * np.sin(theta) + self.center[1]
            z = h - (self.H/2) + self.center[2]
        return np.array([x, y, z])

    def getPoints(self):
        theta_linspace = np.linspace(0, 2*np.pi, self.resolution, endpoint=False)
        h_linspace = np.linspace(0, self.H, self.resolution, endpoint=True)
        r_linspace = np.linspace(0, self.R, self.resolution, endpoint=True)
        vectors = [
            self.getPoint(theta, 0, r) \
                for theta in theta_linspace \
                for r in r_linspace
        ]
        vectors.extend([
            self.getPoint(theta, h, 0) \
                for theta in theta_linspace \
                for h in h_linspace[1:]
        ])
        return np.array(vectors) / self.max

    def getNormalVector(self, theta, h, r):
        if h == 0:
            x = 0
            y = 0
            z = -1
        else:
            x = np.cos(theta) * self.H / np.sqrt(self.R**2 + self.H**2)
            y = np.sin(theta) * self.H / np.sqrt(self.R**2 + self.H**2)
            z = self.R / np.sqrt(self.R**2 + self.H**2)
        return np.array([x, y, z])

    def getNormalVectors(self):
        theta_linspace = np.linspace(0, 2*np.pi, self.resolution, endpoint=False)
        h_linspace = np.linspace(0, self.H, self.resolution, endpoint=True)
        r_linspace = np.linspace(0, self.R, self.resolution, endpoint=True)
        vectors = [
            self.getNormalVector(theta, 0, r) \
                for theta in theta_linspace \
                for r in r_linspace
        ]
        vectors.extend([
            self.getNormalVector(theta, h, 0) \
                for theta in theta_linspace \
                for h in h_linspace[1:]
        ])
        return np.array(vectors)