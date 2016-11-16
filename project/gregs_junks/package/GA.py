import logging
import sys
from operator import attrgetter
from time import sleep
from random import randint, choice

from Model  import Model, Objective, ColorGradient, Path
from Rule   import Rule, DistanceToPoint
from GAFunc import *

grad=ColorGradient(0,0,0,100,200,300)

logArgs= { 
    'filename' : "./GA.log", 
    'level'    : logging.INFO, 
    'fileMode' : 'w', 
    'format'   : "%(asctime)s %(levelname)s:%(message)s"
}
logging.basicConfig( **logArgs) 
logging.info( "Logging init parameters : " + str( logArgs ) ) 

m = Model()
#m.loadMap( "./maps/sample.png" )
m.loadMap( "./maps/sample2.png" )
m.renderMap( 4, showGrid=False ) 
m.setStart( (1,1) ) 
m.findPOI( lambda p,m: m == 3 )

"""
Set objectives 
"""
maxV = sys.maxint
m.addObjective( Objective( "health", 1000, 0, 1000, better = lambda a,b : a > b ) )
m.addObjective( Objective( "steps",  0,    0, maxV, better = lambda a,b : a < b ) ) 
m.addObjective( Objective( "gold",   15,   0, maxV, better = lambda a,b : a > b ) ) 
m.addObjective( Objective( "goal",   0,    0,    1, better = lambda a,b : a > b ) ) 
m.addObjective( Objective( "alive",  1,    0,    1, better = lambda a,b : a > b ) ) 
m.addObjective( Objective( "d2goal", 0,    0,    1, better = lambda a,b : a < b ) ) 

"""
Set rules
"""
m.addRule( Rule.add( "steps", 1 ) )  
m.addRule( Rule.add( "health", -1 ) ) 
m.addRule( Rule.addIf( 6, "gold", 10 ) )
m.addRule( Rule.setIf( 3, "goal", 1 ) ) 
m.addRule( Rule.addIf( 8, "steps", 3) ) 
m.addRule( Rule.addIf( 5, "health", -5 ) )
m.addRule( Rule.addIf( 7, "health", 10 ) ) 
m.addRule( Rule.setIfValue( "health", Rule.lt, 1, "alive", 0 ) ) 
m.addRule( Rule.breakIf( "alive", Rule.eq, 0 ) ) 

m.addPathMetric( DistanceToPoint( "d2goal", (1,m.width-1) ) ) 

m.buildWaypoints( coverage=0.03, renderNetwork=False ) 


logging.info("====================")
logging.info("= GENETIC  PATHING =")
logging.info("====================")

gen     = 0
gens    = 100
mutRate = 0.1
initPop = 200
popSize = 100

logging.info("%15s : %s", "generations", gens)
logging.info("%15s : %s", "inital pop",  initPop)
logging.info("%15s : %s", "pop size",  popSize)
logging.info("%15s : %s", "mutation rate", mutRate)

population = m.generatePaths( initPop, maxLen=50 ) 
elitism( m, population, popSize, bdom )
initial_pop= [ Path(p) for p in population ]
logging.info("paths generated : %d", len(population) )

while gen < gens :
  gen +=1
  logging.info("====GENERATION%02d====", gen)
  children = []
  while( len( children) < 100 ) : 
    mom = choice( population )
    dad = choice( population )
    while( mom == dad ) :
      dad = choice( population )

    child = mutate( m, crossover(m, mom, dad ), mutRate )
    if (    m.validPath( child ) 
        and child not in population 
        and child not in children
    ):
      children.append(child)

  population = elitism(m, children+population, popSize, bdom )
  logging.info( "population size : %d", len(population ) )
  for i, p in enumerate(population[:10]) :
    m.reset()
    m.draw_path( p, grad )
    m.draw_text( 0, "generation %d, individual %d"%(gen, i), "black" ) 
    m.draw_text( 1, "fitness=%d"%(p.fitness), "black")
    m.draw_text( 3, "score=\n%s"%("\n".join(["%s:%s"%(str(k),str(v)) for k, v in p.score.iteritems()])), "black")
    m.update()
 
  


