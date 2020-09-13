from __future__ import division, print_function
from image import Image
from color import Color
import numpy


width = 256
height = 256

im = Image(width, height)

for j in range(height):
    for i in range(width):
        clr = Color(j/(width-1), i/(height-1), 0.25)
        clr = clr.colorvec
        im.pixels[i][j] = clr

im.makeimage( 'first.ppm' )


