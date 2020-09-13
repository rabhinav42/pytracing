from __future__ import division, print_function
from numpy import linalg
class Ray:
    def __init__(self, orig, direc):
        self.orig = orig
        if linalg.norm(direc) == 0:
            self.direc = direc
        else:
            self.direc = direc/linalg.norm(direc)

    def at(self, t):
        """ position vector at t """
        return self.orig + self.direc * t
