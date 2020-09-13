from __future__ import division, print_function
from sphere import Sphere
from image import Image, Camera, render
from color import Color, Lambertian, Metal, Dielectric
from hittables import Hittables
import numpy
from numpy.linalg import norm
from random import random
from utils import randinrange


def random_balls():
    wrld = []
    wrld.append(Sphere(numpy.array([0, -1000, 0]), 1000, Lambertian(numpy.array([0.5, 0.5, 0.5]))))

    for i in range(-4, 4):
        for j in range(-4, 4):
            choice = random()
            center = numpy.array([i + 0.9 * random(), 0.2, j + 0.9 * random()])

            if norm(center - numpy.array([4, 0.2, 0])) > 0.9:
                if choice < 0.33:
                    albedo = numpy.random.rand(3)
                    wrld.append(Sphere(center, 0.2, Lambertian(albedo)))

                elif choice < 0.66:
                    albedo = 0.5 + 0.5 * numpy.random.rand(3)
                    fuzz = randinrange(0, 0.5)
                    wrld.append(Sphere(center, 0.25, Metal(albedo, fuzz)))

                else:
                    wrld.append(Sphere(center, 0.3, Dielectric(1.5)))

    wrld.append(Sphere(numpy.array([0, 1, 0]), -1.0, Dielectric(1.5)))
    wrld.append(Sphere(numpy.array([-4, 1, 0]), 1.0, Lambertian(numpy.array([0.4, 0.2, 0.1]))))
    wrld.append(Sphere(numpy.array([4, 1, 0]), 1.0, Metal(numpy.array([0.7, 0.6, 0.5]), 0)))

    return wrld


ar = 16.0 / 9
width = 500
height = round(width / ar)
bounces = 10
samples = 70

world = Hittables(random_balls())
lookfrom = numpy.array([0, 10, 13])
lookat = numpy.array([0, 0, 0])
ap = 0.1
focus_d = 10.0

camera = Camera(ar, samples, bounces, ap, focus_d, 20, lookfrom, lookat)
im = Image(width, height)

print('RENDERING!')
render(world, camera, im, 'randomscene')
