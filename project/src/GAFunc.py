import logging
from Model import Path
from bresenhams import bresenhams
from operator import attrgetter 
from random import randrange, random, choice

def bdom( model, a, b ) : 
  dom = False
  for obj in model.objs : 
    if( obj.better( a.score[obj.name], b.score[obj.name] ) ) : 
      dom = True
    if( obj.better( b.score[obj.name], a.score[obj.name] ) ) :
      return False
  return dom

def setFitness( model, paths, dom_func ) : 
  for p in paths :
    p.fitness = len([1 for x in paths if dom_func( model, p, x ) ])
 
def crossover( model, mom, dad ) :
  m_index = randrange( 1, len(mom) + 1 ) 
  d_index = randrange( len(dad) )
  mom_end   = mom[m_index-1]
  dad_start = dad[d_index]
  return mom[:m_index] + dad[d_index:] 

def grow( model, mom, grow_rate ) :
  if random() < grow_rate :
    mom.append( choice(model.adjLst[mom[-1]] ) )
  return mom
  
def mutate( model, mom, mutation_rate ) :

  """
  Mutation idea one 
  """
  for i in xrange( 1, len(mom) ) : 
    if random() < mutation_rate :
       mom[i] = choice( model.adjLst[mom[i-1]] )

  return mom
      
def elitism( model, paths, retain_size, dom_func ) :
  setFitness( model, paths, dom_func )
  paths.sort( key=attrgetter('fitness'), reverse=True )
  return paths[:retain_size]

      
      

  

