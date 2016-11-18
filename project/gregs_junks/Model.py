from __future__ import print_function
from PIL import Image

import sys

class Path ( ) : 
   def __init__( self ) : 
      self.data = []

   def __getitem__( self, x ) : 
      self.data.__getitem__( x ) 

   def __setitem__( self, x, y) : 
      selfdata.__setitem__(x, y)


class Model ( ) : 

   def __init__( self, mapFile ) : 
       self.map = makeMap( mapFile )
        

if __name__ == "__main__" : 
    m = Model( sys.argv[1] )
