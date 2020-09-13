from __future__ import division, print_function
from math import pi, sin, cos, acos, sqrt
from random import random
import numpy


def degrees_to_rad(deg):
    return deg * pi / 180


def normalize(v):
    return v / numpy.linalg.norm(v)


def random_unit_sphere():
    theta = randinrange(0, 2 * pi)
    v = randinrange(0, 1)
    phi = acos((2 * v) - 1)
    r = pow(random(), 1.0 / 3.0)
    return numpy.array([r * sin(phi) * cos(theta), r * sin(phi) * sin(theta), r * cos(phi)])


def random_in_hemisphere(normal):
    unitsp = random_unit_sphere()
    if numpy.dot(unitsp, normal) > 0.0:
        return unitsp
    return -unitsp


def random_unit_disk():
    theta = randinrange(0, 2 * pi)
    r = random()
    return numpy.array([r*cos(theta), r*sin(theta), 0])


def randinrange(x0, x1):
    return x0 + (x1 - x0) * random()


def reflect(v, n):
    return v - 2 * numpy.dot(v, n) * n


def refract(v, n, eta_ratio):
    cos_theta = numpy.dot(-v, n)
    r_par = eta_ratio * (v + (cos_theta * n))
    r_perp = -sqrt(1 - numpy.dot(r_par, r_par)) * n
    return r_par + r_perp


def schlick(cos_theta, eta):
    r0 = pow((1 - eta) / (1 + eta), 2)
    return r0 + (1 - r0) * pow(1 - cos_theta, 5)
