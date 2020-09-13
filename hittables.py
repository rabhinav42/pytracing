from __future__ import division, print_function
from math import inf


class Hittables:
    def __init__(self, hittables):
        self.hittables = hittables

    def hit(self, r):
        """ get info about the first object hit by ray r """
        closest = 1000.0
        hitobj = None
        anyhit = False

        for hittable in self.hittables:
            info = hittable.hit(r)
            if info is not None:
                if info['dist'] < closest:
                    anyhit = True
                    hitobj = hittable
                    closest = info['dist']
                    hitinfo = info

        if anyhit:
            return hitobj, hitinfo
        else:
            return None
