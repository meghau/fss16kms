from __future__ import division

import logging
from random      import randrange, random, uniform
from time        import sleep
from bresenhams  import bresenhams
from operator    import lt, gt, eq
from Tkinter     import Tk, Canvas
from collections import defaultdict, namedtuple 
from PIL         import Image
from Rule        import Rule, Constraint, DistanceToPoint

Objective = namedtuple( "Objective", ["name", "start", "min", "max", "better"] )

class Path( object ) : 
  def __init__( self, pos_list ) : 
    self.data    = pos_list[:]
    self.score   = None
    self.invalid = False 
    self.fitness = None
  def __eq__     ( self, y ) :   return self.data == y.data
  def __getitem__( self, x ) :   return self.data[x]
  def __setitem__(self, x, y ) : self.data[x] = y
  def __len__( self ) :          return len( self.data ) 
  def __iter__( self ) : 
    for x in self.data : 
      yield x 

  def walk( self ) :
    for i in xrange( len(self) -1 ) :
      for p in bresenhams( self[i], self[i+1] ) : 
        if( p != self[i+1] ) : 
          yield p
    yield self[-1]

  def __str__( self ):
    return (
      "Path(len = %d,invalid=%s,score=%s)"%(
        len(self), 
        str(self.invalid), 
        str(self.score) if self.score else "None"
      )
    )

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

grad=ColorGradient(0,0,0,100,200,300)
    
class Model( object ) :

  def __iter__( self ) :
    for r in xrange( self.height ) :
      for c in xrange( self.width ) :
        yield ((r,c), self.map[r][c] )
    
  def __setitem__( self, x, y ):
    assert isinstance( x, tuple ), "model must be reference using a 2D point tuple of (row, col)"
    self.map[x[0]][x[1]] = y

  def __init__( self ) :
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
    self.objs   = []
    self.rules  = []
    self.consts = []
    self.metrics= []
    logging.info( "Model inititalized" ) 

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
        self.poi.append( p ) 

  def dom(self, a, b ) : 
    if( self.bdom == True ) :
      exit(1)
    else : 
      exit(1)

  def addObjective( self, obj ) : self.objs.append( obj ) 
  def addRule( self, rule )     : self.rules.append( rule ) 
  def addMetric( self, metric ) : self.metrics.append( metric )
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

  def newPath( self, p_list ) :

    path  = Path( p_list )
    upnts = set()
    pnts  = 0 

    path.score = { x.name : x.start for x in self.objs }

    try : 
      for p in path.walk() : 

        pnts += 1
        upnts.add( p ) 

        if self.map[p[0]][p[1]] == 0 :
          path.invalid = True 
          return path

        [ r( path.score, p, self.map[p[0]][p[1]] ) for r in self.rules ] 

      for o in self.objs : 
        path.score[o.name] = min(max( path.score[o.name], o.min ), o.max)

      for met in self.metrics : 
        met.score( self, path.score, path ) 

    except:
      logging.info("EXCEPT")
      path.invalid = True
      return path

    path.score["exploration"] = float( len(upnts)) / float(pnts) 
    path.invalid = path.invalid or any([ not c( path.score ) for c in self.consts ])
    return path

  def getColor( self, v ) : 
    return self.color[ v ]

  def getWaypoints( self, coverage, renderNetwork=True, renderCoverage=False, color=None ) :

    """
    Build a waypoints map. A hacky way to make random paths. 
    Add poi, calculate the coverage then add random points until coverage is 
    at or above threshold
    """

    grad        = color if color else ColorGradient( 4095,0,4095,20,0,5)
    waypoints   = set() 
    adjLst      = defaultdict( list )  
    open_space  = len([1 for p,v in self if v != 0 ])
    givenpoints = [ self.start ] + self.poi

    cur_coverage = 0
    while( cur_coverage < coverage ) :

      newpoint = givenpoints.pop() if givenpoints else (randrange(self.height-1), randrange(self.width-1))
      
      if( self.map[newpoint[0]][newpoint[1]] == 0 ): continue

      for waypoint in list( waypoints ) :
        walls = len([1 for p in bresenhams( waypoint, newpoint ) if self.map[p[0]][p[1]] == 0 ])
        if walls == 0:
          adjLst[waypoint].append(newpoint)
          adjLst[newpoint].append(waypoint)

      waypoints.add( newpoint )

      if renderNetwork :
        self.draw_oval( newpoint, grad )
        for dest in adjLst[ newpoint ] :
          self.draw_line( newpoint, dest, grad )
        if len(waypoints) % 75 == 0 : 
          self.update()
 
      if renderCoverage :
        for dest in adjLst[ newpoint ] :
          for p in bresenhams( newpoint, dest ) :
            self.draw_rect( p, grad )
        self.update()

      cur_coverage = len( waypoints ) / open_space  #integer division.
   
    logging.info( "Waypoints : %d, Coverage %f%%", len(waypoints), cur_coverage * 100 )
    return adjLst

  def simpleSeedPaths( self, n ) :
    return [ self.newPath( [self.start] ) for _ in xrange( n ) ]

  def generatePaths( self, n, adjLst, maxLen=10, showPaths=False ) : 
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
      maxLen = len( adjLst.keys() ) / 5

    paths  = []
    misses = 0 
    while( len( paths ) < n ) :

      if misses > 5 :
        maxLen = maxLen + (maxLen // 10 )
        logging.info("Extending maxLen to %d", maxLen )
        misses = 0

      path = [self.start]
      while len( path ) < maxLen : 
        npos = weighted_choice( adjLst[path[-1]], weights )
        path.append( npos ) 
        if( self.map[npos[0]][npos[1]] == 3 ):
          break
        else :
          weights[npos] += 1

      path = self.newPath( path )  

      logging.info( path ) 
     
      if showPaths : 
        self.delete( tag="remove" )
        self.draw_path( path, "blue", tag="remove")
        self.update()

      if not path.invalid:
        misses = 0 
        paths.append( path )
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

  def renderPopulation( self, population ) :
    for i, p in enumerate(population[:10]) :
      self.reset()
      self.draw_path( p, grad )
      self.draw_text( 0, "score=\n%s"%("\n".join(["%s:%s"%(str(k),str(v)) for k, v in p.score.iteritems()])), "black")
      self.update()

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

  @staticmethod
  def example( k ) :
    if k == 1 : 
      m = Model()
      m.loadMap( "./maps/pathGenSample.png" )
      m.setStart( (1,1) ) 
      m.findPOI( lambda p,m : m == 3 )
      
      """
      Set objectives 
      """
      maxV = 100000000000000000

      m.addObjective( Objective( "dStart", 0, 0, maxV, better=gt))
      m.addObjective( Objective( "exploration", 0, 0, 1,  better=gt))
      m.addObjective( Objective( "health", 1000, 0, 1000, better=gt))
      m.addObjective( Objective( "steps",  0,    0, maxV, better=lt)) 
      m.addObjective( Objective( "gold",   15,   0, maxV, better=gt)) 
      m.addObjective( Objective( "goal",   0,    0,    1, better=gt)) 
      m.addObjective( Objective( "alive",  1,    0,    1, better=gt)) 
      
      """
      Set rules
      """
      def ruleSet( score, point, value ) : 
        score["steps"] += 1
        score["health"] -= 1
        if value == 6 : score["gold"] += 10
        if value == 3 : score["goal"] = 1
        if value == 3 : score["gold"] += 100
        if value == 3 : score["health"] += 50
        if value == 8 : score["steps"] += 5
        if value == 5 : score["health"] -= 5
        if value == 7 : score["health"] += 10
        if score["health"] <= 0 : score["alive"] = 0
        if score["goal"] == 1 : return "break"
        
      m.addRule( ruleSet )    
      #m.addRule( Rule.add( "steps", 1 ) )  
      #m.addRule( Rule.add( "health", -1 ) ) 
      #m.addRule( Rule.addIf( 6, "gold", 10 ) )
      #m.addRule( Rule.setIf( 3, "goal", 1 ) ) 
      #m.addRule( Rule.addIf( 3, "gold", 100 ) )
      #m.addRule( Rule.addIf( 3, "health", 50 ) )
      #m.addRule( Rule.addIf( 8, "steps", 4) ) 
      #m.addRule( Rule.addIf( 5, "health", -5 ) )
      #m.addRule( Rule.addIf( 7, "health", 10 ) ) 
      #m.addRule( Rule.setIfValue( "health", lt, 1, "alive", 0 ) ) 
      #m.addRule( Rule.breakIf( "goal", eq, 1 ) ) 

      m.addConstraint( Constraint( "alive", eq, 1 ) )

      m.addMetric( DistanceToPoint( "dStart", m.start ) ) 
      
      return m

    if k == 2 : 
      m = Model()
      m.loadMap( "./maps/sample.png" )
      m.setStart( (1,1) ) 
      m.findPOI( lambda p,m : m == 3 )
      
      """
      Set objectives 
      """
      maxV = 100000000000000000

      m.addObjective( Objective( "dStart", 0, 0, maxV,    better=gt))
      m.addObjective( Objective( "exploration", 0, 0, 1,  better=gt))
      m.addObjective( Objective( "health", 1000, 0, 1000, better=gt))
      m.addObjective( Objective( "steps",  0,    0, maxV, better=lt)) 
      m.addObjective( Objective( "gold",   15,   0, maxV, better=gt)) 
      m.addObjective( Objective( "goal",   0,    0,    1, better=gt)) 
      m.addObjective( Objective( "alive",  1,    0,    1, better=gt)) 
      
      """
      Set rules
      """

      def ruleSet( score, point, value ) : 
        score["steps"] += 1
        score["health"] -= 1
        if value == 6 : score["gold"] += 10
        if value == 3 : score["goal"] = 1
        if value == 3 : score["gold"] += 100
        if value == 3 : score["health"] += 50
        if value == 8 : score["steps"] += 5
        if value == 5 : score["health"] -= 5
        if value == 7 : score["health"] += 10
        if score["health"] <= 0 : score["alive"] = 0
        if score["goal"] == 1 : return "break"
        
      m.addRule( ruleSet )    
      #m.addRule( Rule.add( "steps", 1 ) )  
      #m.addRule( Rule.add( "health", -1 ) ) 
      #m.addRule( Rule.addIf( 6, "gold", 10 ) )
      #m.addRule( Rule.setIf( 3, "goal", 1 ) ) 
      #m.addRule( Rule.addIf( 3, "gold", 100 ) )
      #m.addRule( Rule.addIf( 3, "health", 50 ) )
      #m.addRule( Rule.addIf( 8, "steps", 4) ) 
      #m.addRule( Rule.addIf( 5, "health", -5 ) )
      #m.addRule( Rule.addIf( 7, "health", 10 ) ) 
      #m.addRule( Rule.setIfValue( "health", lt, 1, "alive", 0 ) ) 
      #m.addRule( Rule.breakIf( "goal", eq, 1 ) ) 

      m.addConstraint( Constraint( "alive", eq, 1 ) )

      m.addMetric( DistanceToPoint( "dStart", m.start ) ) 
      
      return m


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
