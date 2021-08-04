from abc import ABCMeta, abstractmethod

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