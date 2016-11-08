import json
import sys
import time

class Blocks() : 
  Stone    = "stone"
  Stone2   = "cobblestone"
  Stone3   = "sandstone"
  Stone4   = "red_sandstone"
  Stone5   = "stonebrick"
  Diamond  = "diamond_block"
  Emerald  = "emerald_block"
  Gold     = "gold_block"
  Brick    = "brick_block"
  Spots    = "red_mushroom_block"
  Magma    = "magma"
  Fence    = "fence"
  Fire     = "fire"
  Redstone = "redstone_block"

class Maps() : 

  map1 = [
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [ 1,  1,  1,  1,  1,  0,  0,  0,  1,  1,  1,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1 ],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 0,  0,  0,  0,  0,  0,'s',  0,  0,  0,  0,  0,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [ 1,  1,  1,  1,  1,  1,'e',  1,  1,  1,  1,  1,  1 ],
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ]
  ]

class Mission() : 

  DEFAULT_Y = 235
  DEFAULT_X = 0
  DEFAULT_Z = 0

  def __init__(self, name) : 
 #   self.host    = MalmoPython.AgentHost()
 #   self.record  = MalmoPython.MissionRecordSpec()
    self.start   = None
    self.goal    = None
    self.map     = self.getMapObj( name ) 
    self.mission = self.makeMap(self.map,Mission.DEFAULT_X,Mission.DEFAULT_Y,Mission.DEFAULT_Z) 
    self.state   = None 
    self.obs     = None
    self.errors  = None
    self.rewards = None

  def getMapObj( self, name ) : 
    if name == "map1" :
      return Maps.map1

  """
  def setup( self, max_retries=3 ) :

    for retry in range(max_retries):
      try:
        self.host.startMission( self.mission, self.record )
        break
      except RuntimeError as e:
        if retry == max_retries - 1:
          raise
        else:
          time.sleep(2)

    self.state = self.host.getWorldState()
    while not self.state.has_mission_begun or not self.state.observations : 
      sys.stdout.write(".")
      time.sleep(0.1)
      self.state = self.host.getWorldState()
      for error in self.state.errors:
        print "Error:",error.text
 
      for obs in self.state.observations : 
        obs = str( obs ) 
        obs = obs[obs.index(",")+2:]
        self.obs = json.loads( str( obs ) )

    return self

  def goTo(self, tup ) :
    self.host.sendCommand( "tp %d %d %d"%tup )

  def refreshState(self ) :
    self.state = self.host.getWorldState() 
    for obs in self.state.observations : 
      obs = str( obs ) 
      obs = obs[obs.index(",")+2:]
      self.obs = json.loads( str( obs ) )

  def makeMap ( self, mapobj, xo, yo, zo ) : 
  
    mission = MalmoPython.MissionSpec()
    mission.forceWorldReset()
    mission.timeLimitInSeconds(1000000)
    mission.setTimeOfDay(600,False )
    mission.startAtWithPitchAndYaw(0,Mission.DEFAULT_Y,0,180,0)
    mission.setViewpoint(2)
    mission.removeAllCommandHandlers()
    mission.allowAllDiscreteMovementCommands()
    mission.allowAllAbsoluteMovementCommands()
    start = None
    goal  = None

    for x,row in enumerate( mapobj ) :
      for z, ele in enumerate( row ) : 
        if( ele == 0 ) :
          mission.drawBlock( xo+x, yo, zo+z, Blocks.Stone2 )
        elif( ele == 1 ) : 
          mission.drawBlock( xo+x, yo, zo+z, Blocks.Stone2 )
          mission.drawBlock( xo+x, yo+1,zo+z, Blocks.Stone2 )
          mission.drawBlock( xo+x, yo+2,zo+z, Blocks.Fence )
        elif( ele == 's' ) : 
          print( xo+x+.5, yo+1.5, zo+z+.5 ) 
          mission.drawBlock( xo+x, yo, zo+z, Blocks.Emerald )
          mission.observeDistance(xo+x+.5, yo+.5, zo+z+.5, "Start" )
          mission.startAtWithPitchAndYaw( xo+x+.5, yo+1.5, zo+z+.5, 0 ,0 ) 
          self.start = ( xo+x+.5, yo+1.5, zo+z+.5 )
        elif( ele == 'e' ) : 
          mission.drawBlock( xo+x, yo, zo+z, Blocks.Diamond )
          mission.observeDistance(xo+x, yo, zo+z, "End" )
          self.end = ( xo+x+.5, yo+1.5, zo+z+.5 )
        
    return mission
  """
