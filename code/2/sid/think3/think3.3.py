# Think like a Computer Scientist
# Exercise 3.3

def right_justify(s):
	spaces_to_add = 70-len(s)
	print(" "*spaces_to_add+s)

right_justify("Allen")