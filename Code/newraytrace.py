from __future__ import division, print_function
from sphere import Sphere
from image import Image, Camera, ray_color, render
from color import Color, Lambertian, Metal, Dielectric
from hittables import Hittables
import numpy
from joblib import Parallel, delayed
import time
from random import random

start = time.time()
print('Start:{}'.format(start))



ar = 16.0 / 9.0
width = 500
height = round(width / ar)
bounces = 50

s1 = Sphere(numpy.array([0.5, 0, -1]), -0.5, Dielectric(1.5))
s2 = Sphere(numpy.array([0, -1000.5, -1]), 1000, Lambertian(numpy.array([0.6, 0.7, 0.8])))
s3 = Sphere(numpy.array([-0.5, 0, -1]), -0.5, Dielectric(1.5))
s4 = Sphere(numpy.array([1, 0, -1]), 0.6, Metal(numpy.array([0.7, 0.7, 0.7])))
s5 = Sphere(numpy.array([-1, 0, -1]), 0.6, Metal(numpy.array([0.5, 0.7, 0.8])))

world = Hittables([s1, s2, s3, s4, s5])
camera = Camera(ar, 50, bounces, lookfrom=numpy.array([3, 3, 2]), lookat=numpy.array([0, 0, -1]))

im = Image(width, height)

render(world, camera, im, 'test')

end = time.time()


print('End: {}'.format(end))
print('Diff: {}'.format(end - start))
