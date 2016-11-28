#!python
from __future__ import print_function

import logging
import sys

from Model     import Model
from GA        import GA
from threading import Thread

class GAThread(Thread) : 

  def __init__( self,
    m, 
    initPaths=[],
    genPaths=0,
    coverage=0.2
  ) : 
    super(GAThread, self).__init__( target=self ) 
    self.model    = m
    self.ret      = None 
    self.coverage = coverage
    self.ip       = initPaths
    self.gp       = genPaths

  def __call__( self ) : 

    initPop = self.ip

    if( self.gp != 0 ) :
      adjLst = m.getWaypoints( coverage=self.coverage, renderNetwork=False ) 
      genPop = m.generatePaths( self.gp, adjLst, maxLen=25, showPaths=False )
      initPop += genPop

   # pop = GA(m, initPop, mutator=t, selector=s, gens=10, popSize=25, render=False ) 
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


  t = [ GAThread( m, coverage=0.04, genPaths=x) for x in xrange(10) ] 

  for x in t : 
    x.start() 
  
  for x in t : 
    x.join()

  allPaths = []
  for x in t : 
    allPaths += x.ret 

  print( *map( str, allPaths), sep="\n" ) 

  m.renderPopulation( allPaths ) 
  while ( 1) : pass
