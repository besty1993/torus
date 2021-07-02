import math
import numpy as np
import time
from matplotlib import pyplot as plt

class Torus():
    def __init__(self, R, r, a=0, b=0, c=1, density=100, window_size=(70,35)):
        self.R = R
        self.r = r
        self.density = density
        self.window_size = window_size
        self.setPlane(a=a, b=b, c=c)

    def __call__(self):
        vectors = self.project()
        vectors = self.transformPlane(vectors)
        vectors = self.fitToWindow(vectors)
        return self.print(vectors)

    def getTorusVector(self, theta, phi):
        return np.array([
            (self.R+self.r*math.cos(theta))*math.cos(phi),
            (self.R+self.r*math.cos(theta))*math.sin(phi),
            self.r * math.sin(theta)
        ])

    def setPlane(self, a=0, b=0, c=0):
        norm = np.linalg.norm([a, b, c])
        assert norm > 0
        
        self.plane_vec = np.array([a, b, c])
        self.plane_vec = self.plane_vec / norm

    def project(self):
        projectedVectors = []
        for i, theta in enumerate(np.linspace(0, 2*math.pi, self.density)):
            for j, phi in enumerate(np.linspace(0, 2*math.pi, self.density)):
                vector = self.getTorusVector(theta, phi)
                projected = vector - (np.dot(vector, self.plane_vec) * self.plane_vec)
                projectedVectors.append(projected)

        return np.array(projectedVectors)

    def transformPlane(self, vectors):
        # return vectors[:,:2]

        # https://math.stackexchange.com/questions/1167717/transform-a-plane-to-the-xy-plane
        # https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        # a = self.plane_vec[0]
        # b = self.plane_vec[1]
        # c = self.plane_vec[2]
        # norm = np.linalg.norm(self.plane_vec)
        # cos_theta = c / norm
        # sin_theta = np.linalg.norm([a,b]) / norm
        # u1 = b / norm
        # u2 = a / norm * (-1)
        # rotation_matrix = np.array([
        #     [cos_theta + ((u1**2)*(1-cos_theta)), u1*u2*(1-cos_theta), u2*sin_theta],
        #     [u1*u2*(1-cos_theta), cos_theta + ((u2**2)*(1-cos_theta)), u1*sin_theta*(-1)],
        #     [u2*sin_theta*(-1), u1*sin_theta, cos_theta]
        # ])
        # new_vectors = np.dot(vectors, rotation_matrix)
        # return new_vectors[:,:2]

        v = self.plane_vec                  ## Origin plane vector
        k = np.array([0,0,-1])              ## Target plane vector
        u = np.cross(v, k)                  ## Rotation axis
        cos = v[2]                          ## Cosine of angle between origin and target
        sin = (1 - (cos**2))**0.5           ## Sine of angle between origin and target
        rotation_matrix = np.array([
            [cos+((u[0]**2)*(1-cos)), u[0]*u[1]*(1-cos)-(u[2]*sin), u[0]*u[2]*(1-cos)+(u[1]*sin)],
            [u[1]*u[0]*(1-cos) + (u[2]*sin), cos+((u[1]**2)*(1-cos)), u[1]*u[2]*(1-cos)-(u[0]*sin)],
            [u[2]*u[0]*(1-cos) - (u[1]*sin), u[2]*u[1]*(1-cos)+(u[0]*sin), cos+((u**2)*(1-cos))]
        ])
        new_vectors = np.dot(vectors, rotation_matrix)
        return new_vectors[:,:2]


    def fitToWindow(self, vectors):
        ## Normalize
        vectors = vectors/(self.R+self.r)

        ## Fit to the window
        window = np.array(self.window_size)
        vectors = (vectors+1)*(window//2)
        vectors = vectors.astype(np.int)
        return vectors

    def print(self, vectors):
        # temp = [' '] * (self.window_size[0]+1)
        # temp = [temp] * (self.window_size[1]+1)
        # for v in vectors:
        #     x = v[0]; y = v[1]
        #     temp[y][x] = '@'
        # temp = [''.join(t) for t in temp]
        # return '\n'.join(temp)

        text = [(' '*(self.window_size[0]+1))]*(self.window_size[1]+1)
        for point in vectors:
            x = point[0]; y = point[1]
            text[y] = list(text[y])
            text[y][x]='@'
            text[y] = ''.join(text[y])
        return np.array(text)

        # text = [[' ']*(self.window_size[0]+1)]*(self.window_size[1]+1)
        # for point in vectors:
        #     x = point[0]; y = point[1]
        #     text[y][x]='@'
        # # text[y] = ''.join(text[y])
        # result = [''.join(t) for t in text]
        # return '\n'.join(result)


class CONFIG:
    R = 2
    r = 1

a = Torus(R=CONFIG.R, r=CONFIG.r)

for t in range(100):
    a.setPlane(math.sin(t/10),0,math.cos(t/10))
    # a.setPlane(
    #     a = math.sin(t/5*math.pi),
    #     b = math.cos(t/3*math.pi),
    #     c = math.cos(t/10*math.pi),
    # )
    print(a(), end='\r')
    time.sleep(0.1)