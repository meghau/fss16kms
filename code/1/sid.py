from __future__ import print_function
import random
from utest import ok

@ok
def skynet():
	"""Function to predict if machines will take over the world.
	"""
	did_machines_take_over = False
	random.seed()
	
	if random.random()>0.5:
		print("HelloWorld!")
	else:
		print("WorldDomination!")
		did_machines_take_over = True
	
	assert did_machines_take_over==False