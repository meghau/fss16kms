#!python
from __future__ import print_function

import logging
import sys

from Model       import Model
from GA          import GA, Selector, Mutator
from threading   import Thread
from collections import namedtuple

Objective = namedtuple( "Objective", ["name", "high", "low"] ) 

selector = Selector( dom=Selector.bdom ) 

parms = [
  Objective( "crossover", 0.8, 1),
  Objective( "extend", 0, 1 ),
  Objective( "split", 0, 1 ),
  Objective( "join", 0, 1 ),
  Objective( "move", 0, 1 ),
  Objective( "step_x", 0, 1), 
  Objective( "step_y", 0, 1)
]
  

class GAThread(Thread) : 

  def __init__( self,
    m, 
    initPaths=[],
  ) : 
    super(GAThread, self).__init__( target=self ) 
    self.model    = m
    self.ret      = None 
    self.ip       = initPaths

  def __call__( self ) : 
    pop = GA(m, self.ip, mutator=Mutator(), selector=selector, gens=10, popSize=25, render=False ) 
    self.ret = pop


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
  m.renderMap( 6, showGrid=False ) 

  adjLst = m.getWaypoints( coverage=0.25, renderNetwork=False ) 
  paths = m.generatePaths( 50, adjLst, maxLen=25, showPaths=False )

  for _ in range(5) : 

    newPaths = []
    for _ in xrange(10) :
      newPaths +=  GA(m, paths, mutator=Mutator(), selector=selector, gens=10, popSize=25, render=False) 


    paths = selector( m, newPaths, 25 ) 
    m.renderPopulation( paths ) 

  while ( 1) : pass
