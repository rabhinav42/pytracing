from __future__ import division, print_function
from ray import Ray
from sphere import Sphere
from image import Image
from color import Color
import numpy

width = 500
height = 256

aspect_r = width/height
im = Image(width,height)
camera = numpy.array([0.0,0.0,0.0])
center = numpy.array([0.0,0.0,-1.0])
r = 0.25
sp = Sphere(center, r, 'solid')
x0 = -1.0
x1 = 1.0
y0 = 1.0/aspect_r
y1 = -1.0/aspect_r
xstep = (x1 - x0)/width
ystep = (y1 - y0)/height

for j in range(height):
    y = y0 + ystep * j
    for i in range(width):
        x = x0 + xstep * i
        loc = numpy.array([x,y,-1.0])
        r = Ray(camera, loc - camera )
        info = sp.hit(r)

        if info is None:
            unit_dir = r.direc
            t = 0.5 * (unit_dir[1] + 1.0)
            col =  (1.0 - t) * Color(1.0, 1.0, 1.0).colorvec + t * Color(0.5, 0.7, 1.0).colorvec
            im.pixels[j][i] = col
        else:
            hitloc = info['P']
            normal = info['normal']
            normal = 0.5*(normal + 1)
            im.pixels[j][i] = Color(normal[0], normal[1], normal[2]).colorvec


im.makeimage('firstsphere.ppm')


