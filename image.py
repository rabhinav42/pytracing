from __future__ import division, print_function
from color import ray_color
from random import random
import numpy
from ray import Ray
from math import pi, tan
import sys
from utils import normalize, degrees_to_rad, random_unit_disk
from joblib import Parallel, delayed




class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]

    def makeimage(self, filename):
        """ make an image from given pixel arrangement """
        with open(filename, 'w+') as f:
            f.write('P3\n')
            f.write('{} {} \n'.format(self.width, self.height))
            f.write('255\n')
            for j in range(self.height):
                for i in range(self.width):
                    f.write('{} {} {} '.format(self.pixels[j][i][0], self.pixels[j][i][1], self.pixels[j][i][2]))

        f.close()




class Camera:
    def __init__(self, aspect_r, samples, max_depth, aperture=0.0, focus_dist=1.0, vfov=90.0,
                 lookfrom=numpy.array([0.0, 0.0, 0.0]), lookat=numpy.array([0.0, 0.0, -1.0])):
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.origin = self.lookfrom

        self.up = numpy.array([0, 1, 0])
        self.k = normalize(self.lookfrom - self.lookat)
        self.i = normalize(numpy.cross(self.up, self.k))
        self.j = normalize(numpy.cross(self.i, self.k))

        self.aspect_r = aspect_r
        self.vfov = degrees_to_rad(vfov)
        self.aperture = aperture
        self.lens_radius = aperture / 2
        self.focus_dist = focus_dist  # this stuff works but figure out why
        self.samples = samples
        self.max_depth = max_depth

    def h(self):
        return tan(self.vfov / 2)

    def viewport_h(self):
        return self.h() * 2.0

    def viewport_w(self):
        return self.aspect_r * self.viewport_h()

    def vertical(self):
        return self.viewport_h() * self.j * self.focus_dist

    def horizontal(self):
        return self.viewport_w() * self.i * self.focus_dist

    def lowerleft_corner(self):
        return self.origin - self.horizontal() / 2 - self.vertical() / 2 - (self.k * self.focus_dist)

    def getray(self, u, v):
        rad = self.lens_radius * random_unit_disk()
        offset = self.i * rad[0] + self.j * rad[1]
        origin_off = self.origin + offset
        return Ray(origin_off, self.lowerleft_corner() + u * self.horizontal() + v * self.vertical() - origin_off)


def render(world, camera, im, filename):
    """ renders world and saves it in a ppm file """

    width = im.width
    height = im.height
    max_depth = camera.max_depth

    def p_color(j, i):
        randvec = [(random(), random()) for _ in range(camera.samples)]
        cols = [ray_color(camera.getray((i + p) / (width - 1), (j + q) / (height - 1)),
                          world,
                          max_depth)
                for p, q in randvec]
        return numpy.average(cols, axis=0)

    im.pixels = list(Parallel(n_jobs=4)(delayed(p_color)(j, i) for j in range(height) for i in range(width)))
    im.pixels = [[im.pixels[i] for i in range(start, start + width)] for start in range(0, width * height, width)]

    # randvec = [(random(), random()) for _ in range(camera.samples)]
    # file = sys.stdout
    # prev = 0
    # total = height * width
    # count = 0
    #
    # for j in range(height):
    #     for i in range(width):
    #         count += 1
    #         if count * 100 / total - prev > 1.0:
    #             file.write('\r')
    #             file.write('{}%'.format(round(count * 100 / total)))
    #             prev = count * 100 / total
    #         cols = [ray_color(camera.getray((i + p) / (width - 1), (j + q) / (height - 1)),
    #                           world,
    #                           max_depth)
    #                 for p, q in randvec]
    #
    #         im.pixels[j][i] = numpy.average(cols, axis=0)

    im.makeimage(filename + '.ppm')
    # file.write('\r')
    # file.write('100%')

