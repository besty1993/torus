from abc import ABCMeta, abstractmethod

import numpy as np

class Object3D(metaclass=ABCMeta):
    def __init__(self, center:list, resolution:int):
        """
        Define 3D object
        Args:
            center: The center point of the 3D object. list with length of 3
            resolution: The resolution of the 3d object on the screen.
                        The grid in range of the object parameter will be defined by resolution
        """
        self.center = center
        self.resolution = resolution

    def __call__(self, *args):
        """
        Get points and normal vectors of the 3D object
        Returns:
            points : 3D points of the 3D object
            norms : normal vectors corresponding to points of the 3D object
        """
        points = self.getPoints(*args)
        norms = self.getNormalVectors(*args)
        return points, norms

    @abstractmethod
    def getPoint(self, *args):
        """
        Get a single point defined by parameters
        """
        pass

    @abstractmethod
    def getPoints(self, *args):
        """
        Get all points defined by parameters and each parameter's range
        """
        pass

    @abstractmethod
    def getNormalVector(self, *args):
        """
        Get a single normal vector defined by parameters
        """
        pass

    @abstractmethod
    def getNormalVectors(self, *args):
        """
        Get all normal vectors defined by parameters and each parameter's range
        """
        pass