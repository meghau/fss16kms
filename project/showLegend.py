from __future__ import print_function
from PIL import Image
import sys


colors = [
	"black",
        "grey",
        "dred",
        "red",
        "oj",
        "yellow",
        "greed",
        "blue",
        "purp",
        "white"
]

def _hex( v ):
  t = hex(v)[2:]
  if( len(t) == 1 ) :
      return "0" + t
  else:
      return t
      
def toHex( p ) :
   return "#" + _hex(p[0])+ _hex(p[1])+ _hex(p[2])

im = Image.open("./legend.png")
mat = im.load()

mmap = [ [0] * im.size[1] for _ in range( im.size[0] ) ]

print( "color_name = {" )
for y in xrange( im.size[1] ) :
   p = mat[0,y]
   print( "    \"%s\" : %s,"%(colors[y], str(p)) ) 
print( "}")

print ("colorMap = TwoWayDict()" ) 
for y in xrange( im.size[1] ) :
   p = mat[0,y]
   print( "colorMap[%s] = %s"%(y, str(p)) ) 

print ("colorStr = TwoWayDict()" ) 
for y in xrange( im.size[1] ) :
   p = mat[0,y]
   print( "colorStr[%s] = %s"%(y, toHex(p)) ) 
