import logging
import sys
from operator import attrgetter, lt, gt, eq
from time     import sleep
from random   import randint, choice
from Rule     import Rule
from Model    import Model, Objective, ColorGradient, Path
from GAFunc   import *

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
m.loadMap( "./maps/sample.png" )
#m.loadMap( "./maps/pathGenSample.png" )
#m.loadMap( "./maps/sample2.png" )
m.renderMap( 6, showGrid=False ) 
m.setStart( (1,1) ) 
m.findPOI( lambda p,m: m == 3 )

"""
Set objectives 
"""
maxV = sys.maxint
m.addObjective( Objective( "health", 1000, 0, 1000, better=gt)  )
m.addObjective( Objective( "steps",  0,    0, maxV, better=lt) ) 
m.addObjective( Objective( "gold",   15,   0, maxV, better=gt) ) 
m.addObjective( Objective( "goal",   0,    0,    1, better=gt) ) 
m.addObjective( Objective( "alive",  1,    0,    1, better=gt) ) 

"""
Set rules
"""
#m.addRule( Rule.add( "steps", 1 ) )  
m.addRule( Rule.add( "health", -1 ) ) 
m.addRule( Rule.addIf( 6, "gold", 10 ) )
m.addRule( Rule.setIf( 3, "goal", 1 ) ) 
m.addRule( Rule.addIf( 3, "gold", 1000 ) )
m.addRule( Rule.addIf( 3, "health", 1000 ) )
#m.addRule( Rule.addIf( 8, "steps", 4) ) 
m.addRule( Rule.addIf( 5, "health", -5 ) )
m.addRule( Rule.addIf( 7, "health", 10 ) ) 
m.addRule( Rule.setIfValue( "health", lt, 1, "alive", 0 ) ) 

#m.addConstraint( Constraint( "alive", Op.eq, 1 ) )

m.buildWaypoints( coverage=0.04, renderNetwork=True ) 


logging.info("====================")
logging.info("= GENETIC  PATHING =")
logging.info("====================")

gen     = 0
gens    = 100
mutRate = 0.1
grwRate = 0.2
initPop = 200
popSize = 100

logging.info("%15s : %s", "generations", gens)
logging.info("%15s : %s", "inital pop",  initPop)
logging.info("%15s : %s", "pop size",  popSize)
logging.info("%15s : %s", "mutation rate", mutRate)
logging.info("%15s : %s", "grow rate", grwRate)

population = m.generatePaths( initPop, maxLen=100, showPaths=False ) 
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

    child = grow(m,mutate( m, crossover(m, mom, dad ), mutRate ), grwRate )
    if (    m.validPath( child ) 
        and child not in population 
        and child not in children
    ):
      children.append(child)

  population = elitism(m, children+population, popSize, bdom )
  logging.info( "population size : %d", len(population ) )
  for i, p in enumerate(population[:10]) :
    logging.info( "Path %s : score %s", i, p.score ) 
    m.reset()
    m.draw_path( p, grad )
    m.draw_text( 0, "generation %d, individual %d"%(gen, i), "black" ) 
    m.draw_text( 1, "fitness=%d"%(p.fitness), "black")
    m.draw_text( 3, "score=\n%s"%("\n".join(["%s:%s"%(str(k),str(v)) for k, v in p.score.iteritems()])), "black")
    m.update()
 
  


