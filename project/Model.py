from __future__ import division

import logging
from random import randrange, random, uniform
from time import sleep
from bresenhams import bresenhams

#Python 2/3 portability
try : 
  from Tkinter import Tk, Canvas
except :
  from tkinter import Tk, Canvas

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
  _id = 1
  def __init__( self, pos_list ) : 
    self.id      = Path._id
    Path._id    += 1
    self.data    = [ p for p in pos_list ]
    self.score   = None
    self.fitness = None

  def __eq__     ( self, y ) :   return self.data == y.data
  def __getitem__( self, x ) :   return self.data[x]
  def __setitem__(self, x, y ) : self.data[x] = y
  def __len__( self ) :          return len( self.data ) 
  def __iter__(self) : 
    for x in self.data : 
      yield x 

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
    
class Model( object ) :

  _id = 0

  def __iter__( self ) :
    for r in xrange( self.height ) :
      for c in xrange( self.width ) :
        yield ((r,c), self[(r,c)] )
    
  def __getitem__( self, x ) :
    if isinstance( x, tuple ) :
      return self.map[x[0]][x[1]]
    else :
      return self.map[x]

  def __setitem__( self, x, y ):
    assert isinstance( x, tuple ), "model must be reference using a 2D point tuple of (row, col)"
    self.map[x[0]][x[1]] = y

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
    self.consts = []
    self.metrics= []
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
    for p,v in self : 
      if( lam(p,v) ) :
        logging.info( "Adding poi %s", p ) 
        self.poi.append( p ) 

  def dom(self, a, b ) : 
    if( self.bdom == True ) :
      exit(1)
    else : 
      exit(1)

  def addObjective( self, obj ) : self.objs.append( obj ) 
  def addRule( self, rule )     : self.rules.append( rule ) 
  def addMetric( self, metric ) : self.metrics.append( metics )
  def addConstraint( self, c )  : self.consts.append( c )

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

    for p,v in self :
      if start is not None : 
        if legend[data[p[1], p[0]+1]] == start:
          self.start = p

      self[p] = legend[data[p[1],p[0]+1]]

  def validPath( self, path ) :

    if( path.score == None ):
      self.scorePath( path )

    for i in xrange( len(path) - 1 ) :
      for p in bresenhams( path[i], path[i+1] ) :
        if self[p] == 0 :
          return False

    for con in self.consts :
      if not con( path.score ) :
        return False 
    
    return True
    
  def scorePath( self, path ) :
    
    if( path.score is not None ) : return path.score

    score = { x.name : x.start for x in self.objs } 

    evalRule = True 
    for i in xrange( len( path ) - 1 ) :
      for p in bresenhams( path[i], path[i+1] ):
        for rule in self.rules : 
          if evalRule :
            ret = rule( score, p, self[p] ) 
            if ret == "break" : 
              evalRule = False
        for o in self.objs : 
          score[o.name] = min(max( score[o.name], o.min ), o.max)

    for met in self.metrics : 
      met.score( self, score, path ) 

    path.score = score
    return score


    if not isinstance( objs, Objective ) : 
      exit(1)
    self.objs.append( objs ) 

  def getColor( self, v ) : 
    return self.color[ v ]
  

  def buildWaypoints( self, coverage, renderNetwork=True, renderCoverage=False, color=None ) :

    """
    Build a waypoints map. A hacky way to make random paths. 
    Add poi, calculate the coverage then add random points until coverage is 
    at or above threshold
    """

    grad        = color if color else ColorGradient( 4095,0,4095,20,0,5)
    waypoints   = set() 
    self.adjLst = defaultdict( list )  
    open_space  = len([1 for p,v in self if v != 0 ])
    givenpoints = [ self.start ] + self.poi

    cur_coverage = 0
    while( cur_coverage < coverage ) :

      newpoint = givenpoints.pop() if givenpoints else (randrange(self.height-1), randrange(self.width-1))
      
      if( self[newpoint] == 0 ): continue

      for waypoint in list( waypoints ) :
        walls = len([1 for p in bresenhams( waypoint, newpoint ) if self[p] == 0 ])
        if walls == 0:
          self.adjLst[waypoint].append(newpoint)
          self.adjLst[newpoint].append(waypoint)

      waypoints.add( newpoint )

      if renderNetwork :
        self.draw_oval( newpoint, grad )
        for dest in self.adjLst[ newpoint ] :
          self.draw_line( newpoint, dest, grad )
        if len(waypoints) % 75 == 0 : 
          self.update()
        
      if renderCoverage :
        for dest in self.adjLst[ newpoint ] :
          for p in bresenhams( newpoint, dest ) :
            self.draw_rect( p, grad )
        self.update()

      cur_coverage = len( waypoints ) / open_space  #integer division.
      logging.info( "Waypoints : %d, Coverage %f%%", len(waypoints), cur_coverage * 100 )

  def buildWaypoints_deprcated( self, waypoints=None, renderNetwork=False, renderCoverage=False ) : 

    #TODO : lets make this record coverage as it goes and use it 
    #       as a termination condition.

    #TODO : Better yet yank out the whole random waypoint system and 
    #       give it a visibility map -- that can give perfect coverage
    #       in a whole lot less time -- but that'll take a while to code xx.
    
    """ 
    Lets generate a set of random path segements and a navigation graph
    will return a %percent of the open space in the map searched. 
    """

    if waypoints is None : 
      waypoints = ( self.height * self.width ) / 40

    pnts = set()
    pnts.add( self.start ) 
    map( lambda i : pnts.add( i ), self.poi )

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

    """
    Visuals of the waypoint map
    """
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

  def generatePaths( self, n, maxLen=10, showPaths=False ) : 
    """
    Function for generating a set of random paths 
    My first attemp chose any of a random set of neighbors
    per waypoint, but this meant I didnt hit a lot of waypoints. 
    Using a weighted neighbor choice that prioritizes rarely used neighbors
    first help to cover more of the map in the initial baseline
    search. 
    """

    if showPaths : 
      self.reset() 

    weights = defaultdict( lambda : 0 ) 

    if maxLen is None : 
      maxLen = len( self.adjLst.keys() ) / 5

    paths  = []
    misses = 0 
    while( len( paths ) < n ) :

      if misses > 5 :
        maxLen = maxLen + (maxLen // 10 )
        logging.info("Extending maxLen to %d", maxLen )
        misses = 0

      path = [self.start]
      while len( path ) < maxLen : 
        npos = weighted_choice( self.adjLst[path[-1]], weights )
        path.append( npos ) 
        if( self.map[npos[0]][npos[1]] == 3 ):
          break
        else :
          weights[npos] += 1

      path = Path(path)

      if showPaths : 
        self.delete( tag="remove" )
        self.draw_path( path, "blue", tag="remove")
        self.update()
      if self.validPath( path ) :
        logging.info( "Path %d found", len( paths ) )
        misses = 0 
        paths.append( Path(path) )
        if showPaths : 
          self.draw_path( path, "black")
      else : 
        misses += 1

    return paths

    
  def renderMap( self, scale, showGrid=True ) :

    width = 1 if showGrid else 0

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

    for p,v in self : 
       self.draw_rect( p, self.getColor( v ), tag="map", width=width ) 
    
    self.update()
  
  """
  Helper functions for easy drawing
  """
  def draw_oval( self, p, color, tag="overlay" ) :
    c = color() if callable( color ) else color
    self.canvas.create_oval( 
       p[1]       * self.scale,  p[0]      * self.scale, 
      (p[1] + 1 ) * self.scale, (p[0] + 1) * self.scale, 
      fill=c, tag=tag
    )

  def draw_rect( self, p, color, tag="overlay", width=1 ) :
    c = color() if callable( color ) else color
    self.canvas.create_rectangle( 
       p[1]       * self.scale,  p[0]      * self.scale, 
      (p[1] + 1 ) * self.scale, (p[0] + 1) * self.scale, 
      fill=c, tag=tag, width=width
    )

  def draw_line( self, p1, p2, color, tag="overlay" ) :
    c = color() if callable( color ) else color
    self.canvas.create_line( 
      ( p1[1] + .5 ) * self.scale, ( p1[0] + .5 ) * self.scale, 
      ( p2[1] + .5 ) * self.scale, ( p2[0] + .5 ) * self.scale, 
      fill=c, tag=tag
    )

  def draw_text( self, pos, s, color ) :
    c = color() if callable( color ) else color
    self.canvas.create_text( 50, (self.scale*(self.height+4)) + (30*pos), text=s, tag="overlay", fill=c )

  def draw_path( self, path, color, drawWaypoints=True, tag="overlay" ) :

    for i in xrange( len( path) - 1 ) :
      if( drawWaypoints ) : self.draw_oval( path[i], color, tag=tag ) 
      self.draw_line( path[i], path[i+1], color, tag=tag ) 
    if( drawWaypoints ) : self.draw_oval( path[-1], color, tag=tag ) 

  def update( self ) :
    self.canvas.update()

  def reset ( self, tag="overlay" ) : self.canvas.delete( tag )
  def delete( self, tag="overlay" ) : self.canvas.delete( tag )

  def testBresenhams( self,  p0, p1 ) : 
    """
    Make sure the bresenhams is fully tracing the line
    """
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

def weighted_choice(c, weights ):
   w = [ weights[x]^2 for x in c ]
   w = [ max(w) - x for x in w ]
   total = sum(w)
   r = uniform(0, total)
   upto = 0
   for c, w in zip( c, w ):
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def getColorString( p ) : 
  return "#%02x%02x%02x"%p[0:3]
