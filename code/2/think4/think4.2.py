#exercise 4.2
#Think Python

from __future__ import division
import math

def polygon(t,n, length):
    angle = 360/n
    polyline(t, n, length, angle)

def polyline(t, n, length, angle):
    for i in range(n):
        fd(t, length)
        lt(t, angle)

def arc(t,r,angle):
    sides=50
    length = (math.pi/180)*angle*r
    sides = int(length/3)+1
    polyline(t,sides,length/sides,angle/sides)

def petal(t,r,angle):
    for i in range(2):
        arc(t,r,angle)
        lt(t,180-angle)

def flower(t,r,n,angle):
    """draw Flower with n petals
    """
    for i in range(n):
        petal(t,r,angle)
        lt(t,360/n)

if __name__ == "__main__":
    from swampy.TurtleWorld import *
    world = TurtleWorld()
    bob = Turtle()
    bob.delay = 0.001
    flower(bob,100,7,60)
    wait_for_user()