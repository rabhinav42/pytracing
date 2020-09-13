from __future__ import division, print_function
from math import sqrt
from numpy import dot


class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r):
        """ get info about point on sphere hit by ray r """
        AC = r.orig - self.center
        # a = 1  assume directions are unit vecs
        half_b = dot(r.direc, AC)
        c = dot(AC, AC) - self.radius * self.radius
        det = half_b * half_b - c
        if det > 0:
            dist = (-half_b - sqrt(det))
            if dist > 0.001:
                p = r.at(dist)
                normal = (p - self.center) / self.radius
                ray_inside = dot(normal, r.direc) > 0.0
                normal = -normal if ray_inside else normal
                return {'P': p, 'normal': normal, 'dist': dist, 'ray_inside': ray_inside}
        return None
