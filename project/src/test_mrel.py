from Model_rel import *

p = Path( ( (1,1),(5,0),(6,8),(-2,-4) ) )

for x in p.walk() : 
  print x

