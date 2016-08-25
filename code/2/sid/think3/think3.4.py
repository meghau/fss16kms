# Exercise 3.4

# part 1
def do_twice(f):
	f()
	f()

def print_spam():
	print('spam')

do_twice(print_spam)

# part 2
def do_twice(f,value):
	f(value)
	f(value)

# part 3
def print_twice(str):
	print(str)
	print(str)

# part 4
do_twice(print_twice, "spam")

# part 5
def do_four(f,value):
	do_twice(f, value)
	do_twice(f, value)