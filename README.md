# pytracing
Brute force path tracing engine in python. Adapted from Ray Tracing in One Weekend by Peter Shirley.
newraytrace.py and randomballs.py are examples of how to actually use the engine to make images.
Basic level of parallelism introduced with python's joblib library as well.

Some images:

A random scene generated from randomballs.py:
(https://github.com/rabhinav42/pytracing/blob/master/Images/cap1.JPG)

Odd behaviour of glass because of reflection+refraction: (Middle = glass, surrounding+floor = metal)
(https://github.com/rabhinav42/pytracing/blob/master/Images/glassandmetal.jpg)
