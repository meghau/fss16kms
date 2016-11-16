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
m.renderMap( 12 ) 
m.setStart( (1,1) ) 
m.findPOI( lambda p,m: m == 3 )

"""
Set objectives 
"""
m.addObjective( Objective( "health", 100, 0, 100,  better = lambda a,b : a > b ) )
m.addObjective( Objective( "steps",  0,   0, None, better = lambda a,b : a < b ) ) 
m.addObjective( Objective( "gold",   15,  0, None, better = lambda a,b : a > b ) ) 
m.addObjective( Objective( "goal",   0,   0,    1, better = lambda a,b : a > b ) ) 
m.addObjective( Objective( "alive",  1,   0,    1, better = lambda a,b : a > b ) ) 

"""
Set rules
"""
m.addRule( Rule.add( "steps", 1 ) )  
m.addRule( Rule.add( "health", -1 ) ) 
m.addRule( Rule.addIf( 6, "gold", 10 ) )
m.addRule( Rule.setIf( 4, "goal", 1 ) ) 
m.addRule( Rule.setIfValue( "health", Rule.lt, 1, "alive", 0 ) ) 


waypoints = 10 
coverage  = 0 
while( coverage < 0.80 ) :
   waypoints = waypoints * 2 
   coverage = m.buildWaypoints( waypoints=waypoints, renderNetwork=True ) 
   logging.info("Waypoints = %s, coverage=%3.2f", waypoints, coverage )

paths = m.generatePaths( 100, maxLen=50 ) 

grad = ColorGradient( 4095,4095,4095,100,200,300)
m.reset()
for p in paths :
  m.draw_path( p, grad() ) 
  m.update()

m.reset()
logging.info("====GENERATION 1====")
for i, p in enumerate( paths ) : 
  score = m.scorePath( p ) 
  logging.info( "path %d score : %s", i, score )
  m.draw_path( p, "#000000")
  m.draw_text( 1, "Score\n %s"%("\n".join(["%s:%s"%(str(k),str(v)) for k, v in score.iteritems()])))
  m.update()
  m.reset()

print("Done")
sleep( 10 ) 

