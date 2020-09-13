from __future__ import division, print_function
from abc import ABC, abstractmethod
import numpy
from math import pi, sin, cos, sqrt, acos, pow
from random import random
from ray import Ray
from utils import reflect, refract, random_unit_sphere, random_in_hemisphere, schlick


class Color:
    def __init__(self, r, g, b, maxcol=255):
        self.colorvec = numpy.array([r, g, b])
        self.maxcol = maxcol
        self.colorvec = numpy.sqrt(self.colorvec)  # gamma correction
        self.colorvec = self.intscale(self.maxcol)

    def intscale(self, num=255):
        """ scale up the color vector to num """
        if numpy.sum(self.colorvec) == 0:
            return self.colorvec
        else:
            self.colorvec = numpy.minimum(numpy.round(self.colorvec * num), 255).astype(int)
            return self.colorvec


def ray_color(r, world, depth):
    """ color the point where ray r hits the world """
    if depth <= 0:
        return Color(0, 0, 0).colorvec
    tup = world.hit(r)
    if tup is None:
        unit_dir = r.direc
        t = 0.5 * (unit_dir[1] + 1.0)
        col = (1.0 - t) * Color(1.0, 1.0, 1.0).colorvec + t * Color(0.5, 0.7, 1.0).colorvec
    else:
        info = tup[1]
        hitobj = tup[0]
        scatter_ray = hitobj.material.scatter(info, r)
        if scatter_ray is None:
            return Color(0, 0, 0).colorvec
        attenuation = hitobj.material.albedo
        return attenuation * ray_color(scatter_ray, world, depth - 1)

    return col


class Materials(ABC):
    @abstractmethod
    def scatter(self, info, r):
        pass


class Lambertian(Materials):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, info, r):
        normal = info['normal']
        p = info['P']
        target = p + normal + random_in_hemisphere(normal)
        scatter_ray = Ray(p, target - p)
        return scatter_ray


class Metal(Materials):
    def __init__(self, albedo, blur=0.0):
        self.albedo = albedo
        self.blur = blur if blur < 1 else 1

    def scatter(self, info, r):
        normal = info['normal']
        p = info['P']
        v = r.direc
        ref_v = reflect(v, normal) + self.blur * random_unit_sphere()
        if numpy.dot(ref_v, normal) > 0.0:
            return Ray(p, ref_v)
        else:
            return None


class Dielectric(Materials):
    def __init__(self, eta, albedo=numpy.array([1.0, 1.0, 1.0])):
        self.albedo = albedo
        self.eta = eta

    def scatter(self, info, r):
        normal = info['normal']
        ray_inside = info['ray_inside']
        p = info['P']

        v = r.direc
        cos_theta = numpy.dot(-v, normal)
        sin_theta = sqrt(1 - cos_theta ** 2)
        eta_ratio = self.eta if ray_inside else 1 / self.eta

        if eta_ratio * sin_theta > 1.0:
            return Ray(p, reflect(v, normal))

        if random() < schlick(cos_theta, eta_ratio):
            return Ray(p, reflect(v, normal))

        return Ray(p, refract(v, normal, eta_ratio))
