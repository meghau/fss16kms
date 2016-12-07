colorStr = dict()
colorStr["path"] = 9#"#ffffff" #white
colorStr["wall"] = 0#"#000000" #black
colorStr["start"] = 6#"#22b14c" #green
colorStr["end"] = 3#"#ed1c24" #red
colorStr["fire"] = 4 #orange
colorStr["coin"] = 5 #yellow
colorStr["water"] = 7 #blue
colorStr["magic"] = 8 #purple

def genMap():
	def colorthis(elements, color):
		for i in elements:
			radius = i[0]
			center = i[1]
		
			for x in xrange(center[0]-radius, center[0]+radius):
				for y in xrange(center[1]-radius, center[1]+radius):
					mmap[x][y] = color
		
	def generate_element(p):
		import random as r
		
		number_of_items_range = p[0]
		radius_range = p[1]
		position_range = p[2]

		elements = []
		n = r.randint(number_of_items_range[0], number_of_items_range[1]) 
		for _ in xrange(n):
			radius = r.randint(radius_range[0], radius_range[1])
			position = r.randint(position_range[0], position_range[1]), r.randint(position_range[0], position_range[1])
			elements.append((radius, position))
		
		return elements


	size = 100	
	mmap = [[colorStr["path"]] * size for _ in xrange(size)]
	
	elements = (
	("fire" , (
			(5,10), #number of fires
			(1,3), #radius
			(10,90), #position
			), 
	),
	("coin" , (
			(5,10), #number of coins
			(1,3), #radius
			(10,90), #position
			),
	),
	("water" , (
			(5,10), #number of waters
			(1,3), #radius
			(10,90), #position
			), 
	),
	("magic" , (
			(5,10), #number of magics
			(1,3), #radius
			(10,90), #position
			), 
	),
	("wall" , (
			(5,10), #number of walls
			(5,7), #radius
			(10,90), #position
			)
	)
	)

	
	for e in elements:
		colorthis(generate_element(e[1]), colorStr[e[0]])

	# color the borders
	for x in xrange(size):
		mmap[0][x] = mmap[x][0] = mmap[size-1][x] = mmap[x][size-1] = colorStr["wall"]
	
	# color the start and end
	mmap[1][1] = colorStr["start"]
	mmap[size-2][size-2] = colorStr["end"]
	
	return mmap