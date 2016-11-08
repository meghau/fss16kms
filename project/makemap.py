from __future__ import print_function
from PIL import Image
import sys


im = Image.open(sys.argv[1])
mat = im.load()

mmap = [ [0] * im.size[1] for _ in range( im.size[0] ) ]
for x in xrange( im.size[0] ) :
   for y in xrange( im.size[1] ) :
      p = mat[x,y]
      if( p != ( 255, 255, 255 ) ) :
         mmap[x][y] = 1

print( "mapGen =[")
print( *mmap, sep=",\n" )
print( "]")
