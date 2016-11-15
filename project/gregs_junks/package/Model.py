import logging
import random
from time import sleep
from bresenhams import bresenhams
from Tkinter import Tk, Canvas
from collections import defaultdict
from PIL import Image

def less( a, b ) : return a < b
def more( a, b ) : return a > b
def zero( a, b ) : return abs(a) < abs(b) 

class Objective( object ) :
  def __init__( self, name, start, _min, _max, better=less ):
    self.name   = name 
    self.start  = start
    self.max    = _max
    self.min    = _min
    self.better = better 

class Path( object ) : 
  def __init__( self, pos_list ) : 
    self.data = pos_list
  def __getitem__( self, x ) : 
    return self.data[x]

class ColorGradient( ):
  def __init__( self, r, g, b, r_step, g_step, b_step ) :
    self.r, self.r_step = r, r_step
    self.g, self.g_step = g, g_step
    self.b, self.b_step = b, b_step
  def __call__( self ):
    self.r = (self.r - self.r_step) % 4095
    self.g = (self.g - self.g_step) % 4095
    self.b = (self.b - self.b_step) % 4095
    return "#%03x%03x%03x"%(self.r, self.g, self.b )

class Rule( object ) : 

  def __init__( self, func )       : 
    self.func = func  
  def do( self, score, mapo, pos ) : 
    return self.func( score, mapo, pos ) 

  @staticmethod
  def add( name, value ):
    return Rule( lambda score, mapo, pos : setattr(score, name, getattr(score, name) + value ) )

  @staticmethod
  def addifpos( pos_value, name, value ) :
    return Rule( lambda score, mapo, pos : setattr(score, name, getattr(score, name ) + value ) is mapo[pos[0]][pos[1]] == pos_value )
    


class Model( object ) :

  _id = 0

  def __iter__( self ) :
    for r in xrange( self.height ) :
      for c in xrange( self.width ) :
        yield ( r, c )
    
  def __init__( self ) :

    self.id     = Model._id 
    Model._id   += 1

    self.tk     = None
    self.scale  = -1 
    self.canvas = None
    self.width  = -1 
    self.color  = None
    self.height = -1
    self.overlay= []
    self.start  = (1,1)
    self.poi    = []
    self.map    = None
    self.adjLst = None
    self.objs   = []
    self.rules  = []
    logging.info( "Model %d inititalized"%(self.id) ) 

  def setStart( self, p ) : 
    self.start = p

  def addPOI( self, p ) :
    """
    POI are hints for the random path generation. 
    A big reason for this is to make sure there is a waypoint for every goal
    """
    if isinstance( p, list ) :
      self.poi += p
    else :
      self.poi.append( p ) 
     
  def findPOI( self, lam ) : 
    for p in self : 
      if( lam(p, self.map[p[0]][p[1]]) ) :
        logging.info( "Adding poi %s", p ) 
        self.poi.append( p ) 

  def dom(self, a, b ) : 
    if( self.bdom == True ) :
      exit(1)
    else : 
      exit(1)

  def addRule( self, rule ) :
    rule.parent = self
    self.rules.append( rule ) 
 
  def loadMap( self, mapFile, start=None ) :
    """
    Loads a file in a a map from any basic per pixel form. 
    The fir row of that file is a legend, which numbers colors by the order
    they appear until the first pixel is repeated or all of the pixels are used. 
    """

    if( self.start == None ) : 
      self.start = ( 1,1 ) 

    image = Image.open( mapFile )
    self.height = image.size[1] - 1
    self.width  = image.size[0]

    logging.info( "Loading map : %s [%d,%d]", mapFile, self.height, self.width )
    data = image.load()

   
    i = 1
    legend = {data[0,0]:0}
    self.color = { 0:getColorString( data[0,0] ) }
    while( data[i,0] != data[0,0] ) : 
      legend[data[i,0]] = i 
      self.color[i] = getColorString( data[i,0] )
      i += 1

    self.map = [ [ -1 for _ in xrange( self.width) ] for _ in xrange( self.height ) ] 

    for r,c in self :

      if start is not None : 
        if legend[data[c,r+1]] == start:
          self.start = ( r, c)

      self.map[r][c] = legend[data[c,r+1]]

  def scorePath( self, path ) :
    score = { x.name : x.start for x in self.objs } 
    pos   = self.start

    logging.info( "Score %s", score ) 

    for rule in self.rules : 
      rule.do( score, self.map, pos ) 

    logging.info( "Score %s", score ) 


  def addObjective( self, objs ) :
    if not isinstance( objs, Objective ) : 
      exit(1)
    self.objs.append( objs ) 

  def getColor( self, p ) : 
    return self.color[ self.map[p[0]][p[1]] ]
  
  def drawPath( self, path, color ) :

    for i in xrange( len( path) - 1 ) :
      self.draw_oval( path[i], color() if callable( color ) else color ) 
      self.draw_line( path[i], path[i+1], color() if callable( color ) else color ) 

    self.draw_oval( path[-1], color() if callable( color )  else color ) 
    self.canvas.update()

  def buildWaypoints( self, waypoints=None, renderNetwork=False, renderCoverage=False ) : 
    """ 
    Lets generate a set of random path segements and a navigation graph
    will return a %percent of the open space in the map searched. 
    """

    if waypoints is None : 
      waypoints = ( self.height * self.width ) / 40

    pnts = set()
    pnts.add( self.start ) 
    map( lambda i : pnts.add( i ), self.poi )
    edge = defaultdict( lambda : defaultdict( int ) ) 

    """
    1.) Randomly create a waypoint map. 
    """
    trys = 0 
    while( len(pnts) < waypoints and trys < 2*waypoints ) : 

      trys += 1

      r = random.randint(0,self.height - 1 )
      c = random.randint(0,self.width - 1 )

      if( self.map[r][c] != 0 ) :
        pnts.add( (r,c) )

    """
    2.) Find an interconnectivity network
    """
    self.adjLst = defaultdict( list )


    for p in list( pnts ) : 
      for q in list( pnts ) : 
        if( p == q ) : 
          continue
        valid = True
        for r in bresenhams( p , q ) : 
          if( self.map[r[0]][r[1]] == 0 ):
            valid = False
            break
        if valid :
          self.adjLst[p].append(q)

    if renderNetwork or renderCoverage : 
      self.reset()
      grad = ColorGradient( 4095,0,4095,20,0,5)

      for p, lst in self.adjLst.iteritems():
        for q in lst : 
          if renderCoverage : 
            for r in bresenhams( p, q ) :
              self.draw_rect( r, "#f00" )
          if renderNetwork :
            self.draw_line( p,q, grad() ) 

      self.update()
    open_c = 0 
    for p in self :
      if( self.map[p[0]][p[1]] != 0 ) : 
        open_c += 1

    open_p = set()
    for p, lst in self.adjLst.iteritems() : 
      for q in lst : 
        for r in bresenhams( p, q ) :
          open_p.add( r ) 

    return float( len(open_p) ) / float( open_c ) 

  def generatePaths( self, n, maxLen=None ) : 

    if maxLen is None : 
      maxLen = len( self.adjLst.keys() ) / 10

    paths = []
    for _ in xrange( n ) : 
      path = [self.start]
      while len( path ) < maxLen : 
        npos = random.choice( self.adjLst[path[-1]] )
        path.append( npos ) 
        if( self.map[npos[0]][npos[1]] == 3 ):
          break
      paths.append( path )

    return paths

    
  def renderMap( self, scale ) :

    
    if( self.map == None ):
       logging.error("No map loaded, can not render")
       return 

    if self.tk is None or self.scale != scale :
       self.scale  = scale
       self.tk     = Tk()
       self.canvas = Canvas( self.tk, width=(self.width*scale), height=((self.height*scale)+(2*scale)*len(self.color.keys())), borderwidth=0 )
       self.canvas.pack()


    off = self.height*scale
    for i,k in enumerate( self.color.keys() ) :
       self.canvas.create_rectangle( i*scale*2, off, (i+1)*scale*2, off+(scale*2), fill=self.color[i], tag="map" ) 

    for p in self : 
       self.draw_rect( p, self.getColor( p ), tag="map" ) 
    
    self.update()
  
  """
  Helper functions for easy drawing
  """
  def draw_oval( self, p, color, tag="overlay" ) :
    self.canvas.create_oval( 
       p[1]       * self.scale,  p[0]      * self.scale, 
      (p[1] + 1 ) * self.scale, (p[0] + 1) * self.scale, 
      fill=color, tag=tag
    )

  def draw_rect( self, p, color, tag="overlay" ) :
    self.canvas.create_rectangle( 
       p[1]       * self.scale,  p[0]      * self.scale, 
      (p[1] + 1 ) * self.scale, (p[0] + 1) * self.scale, 
      fill=color, tag=tag
    )

  def draw_line( self, p1, p2, color, tag="overlay" ) :
    self.canvas.create_line( 
      ( p1[1] + .5 ) * self.scale, ( p1[0] + .5 ) * self.scale, 
      ( p2[1] + .5 ) * self.scale, ( p2[0] + .5 ) * self.scale, 
      fill=color, tag=tag
    )

  def update( self ) :
    self.canvas.update()

  def reset ( self, tag="overlay" ) : self.canvas.delete( tag )
  def delete( self, tag="overlay" ) : self.canvas.delete( tag )

  def testBresenhams( self,  p0, p1 ) : 
    self.draw_oval( p0, "#00ff00" ) 
    self.update()
    sleep(0.1)

    self.draw_oval( p1, "#00ff00" ) 
    self.update()
    sleep(0.5)

    for p in bresenhams( p0,p1 ) :
      self.draw_oval( p, "#FF0000" )
      self.update()
      sleep(0.1)


    self.reset()

def getColorString( p ) : 
  return "#%02x%02x%02x"%p[0:3]
