import math
import numpy as np
import time
from matplotlib import pyplot as plt

class Torus():
    def __init__(self, R, r, a=0, b=0, c=0):
        self.R = R      ## The torus center to the tube center
        self.r = r      ## The radius of the tube
        self.a = a      ## X axis
        self.b = b      ## Y axis
        self.c = c      ## Z axis
        self.max = R + r + np.linalg.norm([a, b, c])

    def getPoint(self, theta, phi):
        x = (self.R+self.r*math.cos(theta))*math.cos(phi) + self.a
        y = (self.R+self.r*math.cos(theta))*math.sin(phi) + self.b
        z = self.r * math.sin(theta) + self.c
        return np.array([x, y, z])

    def getPoints(self, density):
        linspace = np.linspace(0, 2*math.pi, density)
        vectors = [
            self.getPoint(theta, phi) \
                for theta in linspace \
                for phi in linspace
        ]
        return np.array(vectors) / self.max

    def getNormalVector(self, theta, phi):
        # https://trecs.se/torus.php
        x = math.cos(theta) * math.cos(phi)
        y = math.sin(theta) * math.cos(phi)
        z = math.sin(phi)
        return np.array([x, y, z])

    def getNormalvectors(self, density):
        linspace = np.linspace(0, 2*math.pi, density)
        vectors = [
            self.getNormalVector(theta, phi) \
                for theta in linspace \
                for phi in linspace
        ]
        return np.array(vectors)



class Render():
    def __init__(self, density=100, window_size=(70,35)):
        self.density = density
        self.window_size = window_size

    def __call__(self, vectors, x_rot=0, y_rot=0, z_rot=0):
        proj = self.rotate(vectors, x_rot, y_rot, z_rot)
        proj = self.project(proj)
        proj = self.fitToWindow(proj)
        return self.print(proj)

    def setProjPlane(self, *args):
        assert len(args) == 3

        norm = np.linalg.norm([*args])
        assert norm > 0
        
        self.plane_vec = np.array([*args])
        self.plane_vec = self.plane_vec / norm

    def setLightVector(self, *args):
        assert len(args) == 3

        norm = np.linalg.norm([*args])
        assert norm > 0
        
        self.light_vec = np.array([*args])
        self.light_vec = self.light_vec / norm
        print(np.linalg.norm(self.light_vec))

    def computeBrightness(self, normal_vectors):
        return np.dot(normal_vectors, self.light_vec)

    def rotate(self, vectors, x_rot, y_rot, z_rot):
        x_matrix = np.array([
            [1,                     0,                     0],
            [0,       math.cos(x_rot),  (-1)*math.sin(x_rot)],
            [0,       math.sin(x_rot),       math.cos(x_rot)],
        ])
        y_matrix = np.array([
            [math.cos(y_rot),       0,       math.sin(y_rot)],
            [0,                     1,                     0],
            [(-1)*math.sin(y_rot),  0,       math.cos(y_rot)]
        ])
        z_matrix = np.array([
            [math.cos(z_rot),       (-1)*math.sin(z_rot),  0],
            [math.sin(z_rot),       math.cos(z_rot),       0],
            [0,                     0,                     1]
        ])
        new_vectors = np.dot(vectors, x_matrix)
        new_vectors = np.dot(new_vectors, y_matrix)
        new_vectors = np.dot(new_vectors, z_matrix)
        return new_vectors

    def project(self, vectors):
        """
        project to xy plane
        """
        z_sizes = np.dot(vectors, self.plane_vec)[:, np.newaxis]
        z_vecs = np.dot(z_sizes, self.plane_vec[np.newaxis,:])
        projected = (vectors - z_vecs)[:,:2]
        return projected

    def fitToWindow(self, vectors):
        window = np.array(self.window_size)
        vectors = (vectors+1)*(window//2)
        vectors = vectors.astype(np.int)
        return vectors

    def print(self, vectors, brightness):
        text = [(' '*(self.window_size[0]+1))]*(self.window_size[1]+1)
        for i, point in enumerate(vectors):
            x = point[0]; y = point[1]
            text[y] = list(text[y])

            # text[y][x]='@'
            if brightness[i] > 0.8:
                text[y][x]='@'
            elif brightness[i] > 0.6:
                text[y][x]='$'
            elif brightness[i] > 0.4:
                text[y][x]='D'
            elif brightness[i] > 0.2:
                text[y][x]='/'
            elif brightness[i] >= 0:
                text[y][x]='*'

            text[y] = ''.join(text[y])
        return np.array(text)


class CONFIG:
    R = 2
    r = 1
    density = 100

if __name__ == '__main__':
    torus = Torus(R=CONFIG.R, r=CONFIG.r)
    points = torus.getPoints(CONFIG.density)
    norm_vectors = torus.getNormalvectors(CONFIG.density)

    renderer = Render()
    renderer.setProjPlane(0,0,1)
    renderer.setLightVector(1,1,1)

    for t in range(100):
        rot_x = 0
        rot_y = 0
        rot_z = t*2*math.pi/10

        proj = renderer.rotate(points, rot_x, rot_y, rot_z)
        norm_vectors = renderer.rotate(norm_vectors, rot_x, rot_y, rot_z)

        proj = renderer.project(proj)
        proj = renderer.fitToWindow(proj)
        brightness = renderer.computeBrightness(norm_vectors)

        print(renderer.print(proj, brightness))
        time.sleep(0.1)