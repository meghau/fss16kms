import logging
from time import sleep
from random import randint 
from Model import Model, Objective, ColorGradient, Rule

logArgs= { 
    'filename' : "./GA.log", 
    'level'    : logging.INFO, 
    'fileMode' : 'w', 
    'format'   : "%(asctime)s %(levelname)s:%(message)s"
}
logging.basicConfig( **logArgs) 
logging.info( "Logging init parameters : " + str( logArgs ) ) 


m = Model()
m.loadMap( "./maps/sample.png" )
m.renderMap( 5 ) 
m.setStart( (1,1) ) 
m.findPOI( lambda p,m: m == 3 )
m.addObjective( Objective( "health", 100, 0, 100,  better = lambda a,b : a > b ) )
m.addObjective( Objective( "steps",  0,   0, None, better = lambda a,b : a < b ) ) 
m.addObjective( Objective( "gold",   15,  0, None, better = lambda a,b : a > b ) ) 
m.addObjective( Objective( "exit",   0,   0,    1, better = lambda a,b : a > b ) ) 


m.addRule( Rule.add( "steps", 1 ) )  

waypoints = 10 
coverage  = 0 
while( coverage < 0.80 ) :
   waypoints = waypoints * 2 
   coverage = m.buildWaypoints( waypoints=waypoints, renderNetwork=True ) 
   logging.info("Waypoints = %s, coverage=%3.2f", waypoints, coverage )

paths = m.generatePaths( 100 ) 

grad = ColorGradient( 0,0,0,-50,-100,-150 )
m.reset()
for p in paths : 
  m.drawPath( p, grad() )

for p in paths : 
  m.scorePath( p ) 

print("Done")
sleep( 10 ) 

