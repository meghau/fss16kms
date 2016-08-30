#Exercise 4.3 
#Think Python

from __future__ import division
import math

def turtle_pie(t,r,angle):
	turn_angle = 180-(180-angle)/2
	chord_length = 2*r*math.sin((angle/2)*(math.pi/180))
	fd(t,r)
	lt(t,turn_angle)
	fd(t,chord_length)
	lt(t,turn_angle)
	fd(t,r)

def turtle_pies(t,r,n):
	for i in range(n):
		turtle_pie(t,r,360/n)
		lt(t,180)
	
if __name__ == '__main__':
	from swampy.TurtleWorld import *
	world = TurtleWorld()
	bob = Turtle()
	turtle_pies(bob,100,6)
	wait_for_user()