# Exercise 3.5
#Think Python
# part 1
def do_twice(f,value):
	f(value)
	f(value)

def do_four(f,value):
	do_twice(f, value)
	do_twice(f, value)

def print_2_row_grid(col):
	do_twice(print_2_row_part_grid,col)
	print_horizontal_line(col)
	
def print_2_row_part_grid(col):
	print_horizontal_line(col)
	do_four(print_vertical_line,col)

def print_vertical_line(col):
	print_line(col,"| ","  ")
	
def print_horizontal_line(col):
	print_line(col,"+ ","- ")
	
def print_line(col,v,e):
	part_line = v + ((9//col)*e)
	line = col*part_line + v
	print(line)

print_2_row_grid(2)

# part 2
def print_4_row_grid(col):
	do_four(print_4_row_part_grid,col)
	print_horizontal_line(col)

def print_4_row_part_grid(col):
	print_horizontal_line(col)
	do_twice(print_vertical_line,col)

print_4_row_grid(4)