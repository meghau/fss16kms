from __future__ import print_function
from PIL import Image
from Util import TwoWayDict
import sys
color_name = {
    "black" : (0, 0, 0, 255),
    "grey" : (127, 127, 127, 255),
    "dred" : (136, 0, 21, 255),
    "red" : (237, 28, 36, 255),
    "oj" : (255, 127, 39, 255),
    "yellow" : (255, 242, 0, 255),
    "greed" : (34, 177, 76, 255),
    "blue" : (63, 72, 204, 255),
    "purp" : (163, 73, 164, 255),
    "white" : (255, 255, 255, 255),
}
colorMap = TwoWayDict()
colorMap[0] = (0, 0, 0, 255)
colorMap[1] = (127, 127, 127, 255)
colorMap[2] = (136, 0, 21, 255)
colorMap[3] = (237, 28, 36, 255)
colorMap[4] = (255, 127, 39, 255)
colorMap[5] = (255, 242, 0, 255)
colorMap[6] = (34, 177, 76, 255)
colorMap[7] = (63, 72, 204, 255)
colorMap[8] = (163, 73, 164, 255)
colorMap[9] = (255, 255, 255, 255)
colorStr = TwoWayDict()
colorStr[0] = "#000000"
colorStr[1] = "#7f7f7f"
colorStr[2] = "#880015"
colorStr[3] = "#ed1c24"
colorStr[4] = "#ff7f27"
colorStr[5] = "#fff200"
colorStr[6] = "#22b14c"
colorStr[7] = "#3f48cc"
colorStr[8] = "#a349a4"
colorStr[9] = "#ffffff"


def getMap( filename ) :
    im = Image.open( filename )
    mat = im.load()

    mmap = [ [0] * im.size[0] for _ in range( im.size[1] ) ]
    for x in xrange( im.size[0] ) :
       for y in xrange( im.size[1] ) :
          p = mat[x,y]
          if ( len(  p ) == 3 ) :  
             p = ( p[0], p[1], p[2], 255 )
          mmap[y][x] = colorMap[ p ] 

    return mmap


