#!python
import logging
import sys
from threading import Thread
from operator import itemgetter, gt, lt, eq
from time import sleep
from random import randint, choice, randrange, random
from Model  import Model, Objective, ColorGradient
from Rule   import Rule, Op, Constraint

class Mutator:
 
  def __init__( self, 
    crossover_rate =1.0, 
    extend_rate    =0.3, 
    split_rate     =0.1,
    join_rate      =0.3,
    move_rate      =0.1, 
    step_size_x    =5, 
    step_size_y    =5,
  ) :
    self.crossover_rate = crossover_rate
    self.extend_rate    = extend_rate 
    self.split_rate     = split_rate 
    self.join_rate      = join_rate
    self.move_rate      = move_rate 
    self.step_size_x    = step_size_x
    self.step_size_y    = step_size_y

  def __call__( self, model, mom, dad ) : 

    new = []
    if random() < self.crossover_rate and len(mom) > 3 and len(dad) > 3 : 
       m_index = randrange( 1, len(mom) + 1 ) 
       d_index = randrange( len(dad) )
       new = mom[:m_index] + dad[d_index:] 
    else :
       new = mom.data[:]

    while random() < self.extend_rate : 
       new.append( ( new[-1][0] + randint( -self.step_size_x, self.step_size_x ), 
                     new[-1][1] + randint( -self.step_size_y, self.step_size_y )
                 ) ) 

    while random() < self.join_rate and len( new ) > 3 : 
      idx = randint( 0,len(new) - 1 )
      del new[idx]

    while random() < self.move_rate:
      idx = randint( 0, len(new) - 1 )
      new[idx] = ( 
         new[idx][0] + randint( -self.step_size_x, self.step_size_x ) ,
         new[idx][1] + randint( -self.step_size_y, self.step_size_y ) 
      )

    return model.newPath( new )

class Selector():
  
  def __init__( self, dom=None ) : 
    self.dom = dom if dom is not None else Selector.bdom 

  def __call__( self, model, pop, k ) :

    def myFitness( me ):
      return len( [1 for other in pop if self.dom( model, me, other ) ] )

    fitnesses = [ (myFitness(x),x) for x in pop ]
    fitnesses.sort( key=itemgetter(0), reverse=True )
    
    return [ x[1] for x in fitnesses[:k] ]

  @staticmethod
  def bdom( model, a, b ) : 
    dom = False
    for obj in model.objs : 
      if( obj.better( a.score[obj.name], b.score[obj.name] ) ) : 
        dom = True
      if( obj.better( b.score[obj.name], a.score[obj.name] ) ) :
        return False
    return dom

  @staticmethod
  def cdom( model, a, b ): 
    raise NotImplemented("Need to do cdom")

    

def GA( m,
     initial_population,
     gens=100, 
     popSize=100, 
     mutator=None, 
     selector=None,
     render=True
   ):

  if mutator is None:
    mutator = Mutator()

  if selector is None:
    selector = Selector() 
  
  
  logging.info("====================")
  logging.info("= GENETIC  PATHING =")
  logging.info("====================")
  logging.info("%15s : %s", "generations", gens)
  logging.info("%15s : %s", "pop size",  popSize)

  population = selector( m, initial_population, popSize ) 

  logging.info( len( population ) )

  gen = 0 
  while gen < gens :
    gen +=1
    logging.info("====GENERATION%02d====", gen)
    children = []
    while( len( children) < 100 ) : 

      mom = choice( population )
      dad = choice( population )

      child = mutator(m, mom, dad ) 

      if ( not child.invalid 
        and child not in population
        and child not in children
      ) : 
        children.append(child)
  
    population = selector( m, population + children, popSize ) 
    logging.info( "population size : %d", len(population ) )
    if render : 
      m.renderPopulation( population )

  return population
 

if __name__ == '__main__' : 

  logArgs= { 
      'filename' : "./GA.log", 
      'level'    : logging.INFO, 
      'fileMode' : 'w', 
      'format'   : "%(asctime)s %(levelname)s:%(message)s"
  }

  logging.basicConfig( **logArgs) 
  logging.info( "Logging init parameters : " + str( logArgs ) ) 

  m = Model.example(2)
  m.renderMap( 4, showGrid=False ) 
  adjLst = m.getWaypoints( coverage=0.2, renderNetwork=False ) 
  pop    = m.generatePaths( 50, adjLst, maxLen=25, showPaths=False ) 

  GA( m, pop, mutator=Mutator(), selector=Selector(), gens=10, popSize=25, render=False ) 
