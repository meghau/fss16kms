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
    initPath=[],
  ) : 
    super(GAThread, self).__init__( target=self ) 
    self.model    = m
    self.ret      = None 
    self.ip       = initPath[:]

  def __call__( self ) : 

    adjLst = m.getWaypoints( coverage=0.02, renderNetwork=False ) 
    paths = m.generatePaths( 20, adjLst, maxLen=25, showPaths=False )

    pop = GA(
       m, 
       self.ip + paths, 
       mutator=Mutator(), 
       selector=selector, 
       gens=3, 
       popSize=15, 
       render=False 
    ) 
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

  m = Model.example(1)
  m.renderMap( 4, showGrid=False ) 

  adjLst = m.getWaypoints( coverage=0.02, renderNetwork=False ) 
  paths = m.generatePaths( 50, adjLst, maxLen=25, showPaths=False )

  for _ in range(10) : 

    t = [ GAThread( m, initPath=paths ) for _ in xrange(3) ]
    [ x.start() for x in t ] 
    [ x.join()  for x in t ] 

    for x in t : 
      newPaths = x.ret 

    paths = selector( m, newPaths, 20 ) 
    m.renderPopulation( paths ) 

  while ( 1) : pass
