import math
from collections import Counter
import numpy as np
import time
from matplotlib import pyplot as plt

class Torus():
    def __init__(self, R, r, a=0, b=0, c=0):
        # https://web.cs.ucdavis.edu/~amenta/s12/findnorm.pdf
        self.r_b = R      ## The torus center to the tube center
        self.r_l = r      ## The radius of the tube
        self.a = a      ## X axis
        self.b = b      ## Y axis
        self.c = c      ## Z axis
        self.max = R + r + np.linalg.norm([a, b, c])

    def getPoint(self, theta, phi):
        """
        Get a single point defined by theta and phi
        Args :
            theta : angle from the tube center to the tube surface
            phi : Angle from the torus center to the tube center
        """
        x = (self.r_b+self.r_l*math.cos(theta))*math.cos(phi) + self.a
        y = (self.r_b+self.r_l*math.cos(theta))*math.sin(phi) + self.b
        z = self.r_l * math.sin(theta) + self.c
        return np.array([x, y, z])

    def getPoints(self, density):
        """
        Get all points defined by grided theta and phi
        Args :
            density : The density of grid of theta and phi
        """
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
        y = math.cos(theta) * math.sin(phi)
        z = math.sin(theta)
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

    def computeBrightness(self, normal_vectors):
        return np.dot(normal_vectors, self.light_vec)

    def move(self, points, x_dist, y_dist, z_dist):
        points += np.array([x_dist, y_dist, z_dist])
        return points

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

    def filterByNormalVectors(self, points, norms):
        inners = np.dot(norms, self.plane_vec)
        points = points[inners>=0]
        norms = norms[inners>=0]
        return points, norms

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
            b = brightness[i]
            
            if b > 0.8:
                text[y][x]='@'
            elif b > 0.6:
                text[y][x]='$'
            elif b > 0.4:
                text[y][x]='|'
            elif b > 0.2:
                text[y][x]='+'
            elif b > 0.1:
                text[y][x]='-'
            else:
                text[y][x]='·'

            text[y] = ''.join(text[y])
        return np.array(text)


class CONFIG:
    R = 2
    r = 1
    density = 200

if __name__ == '__main__':
    torus = Torus(R=CONFIG.R, r=CONFIG.r)
    points = torus.getPoints(CONFIG.density)
    norm_vectors = torus.getNormalvectors(CONFIG.density)

    renderer = Render()
    renderer.setProjPlane(0,0,1)
    renderer.setLightVector(1,1,1)

    for t in range(100):
        rot_x = 0
        rot_y = t*2*math.pi/100
        rot_z = 0

        rot_points = renderer.rotate(points, rot_x, rot_y, rot_z)
        rot_norms = renderer.rotate(norm_vectors, rot_x, rot_y, rot_z)

        rot_points, rot_norms = renderer.filterByNormalVectors(rot_points, rot_norms)

        proj = renderer.project(rot_points)
        proj = renderer.fitToWindow(proj)
        brightness = renderer.computeBrightness(rot_norms)

        print(renderer.print(proj, brightness))
        time.sleep(0.1)