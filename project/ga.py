#!python
from __future__ import division, print_function
import datetime
import logging
import sys, math
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
       m_index = randrange( 2, len(mom) + 1 ) 
       d_index = randrange( len(dad) )
       new = mom[:m_index] + dad[d_index:] 
    else :
       new = mom.data[:]

    while random() < self.extend_rate : 
       new.append( ( new[-1][0] + randint( -self.step_size_x, self.step_size_x ), 
                     new[-1][1] + randint( -self.step_size_y, self.step_size_y )
                 ) ) 

    while random() < self.join_rate and len( new ) > 3 : 
      idx = randint( 2,len(new) - 1 )
      del new[idx]

    while random() < self.move_rate:
      idx = randint( 2, len(new) - 1 )
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
  def cdom(model, a, b):
    def w(better):
      return -1 if better == lt else 1
    def expLoss(w,x1,y1,n):
      return -1*math.e**( w*(x1 - y1) / n )
    def norm(obj,x):
      tmp= (x - obj.min) / (obj.max - obj.min + 10**-32)
      if tmp > 1: 
        return 1
      elif tmp < 0: 
        return 0
      else: 
        return tmp

    def loss(x, y):
      losses= []
      n = len(x.score)
      for obj in model.objs :
        x1, y1 = x.score[obj.name], y.score[obj.name]
        x1, y1  = norm(obj, x1), norm(obj, y1)
        
        losses += [expLoss( w(obj.better),x1,y1,n)]
        
      return sum(losses)/n

    l1 = loss(a,b)
    l2 = loss(b,a)
    return l1 < l2 


def continuous_distance(model, a, b):
    def w(better):
      return -1 if better == lt else 1
    def expLoss(w,x1,y1,n):
      return -1*math.e**( w*(x1 - y1) / n )
    def norm(obj,x):
      tmp= (x - obj.min) / (obj.max - obj.min + 10**-32)
      if tmp > 1: 
        return 1
      elif tmp < 0: 
        return 0
      else: 
        return tmp

    def loss(x, y):
      losses= []
      n = len(x.score)
      for obj in model.objs :
        x1, y1 = x.score[obj.name], y.score[obj.name]
        x1, y1  = norm(obj, x1), norm(obj, y1)
        
        losses += [expLoss( w(obj.better),x1,y1,n)]
        
      return sum(losses)/n

    l1 = loss(a,b)

    return abs(l1) 

# calculate max min for normalization



def igd(m, new_population):
  global_igd = 0
  for new_cand in new_population:
    global_igd += min([continuous_distance(m,new_cand, best_cand) for best_cand in m.baseline_population])
  return global_igd/len(new_population)


def GA( m,
     initial_population,
     gens=100, 
     popSize=100, 
     mutator=None, 
     selector=None,
     render=True,
     calc_igd = False,
     graph_objectives = False
   ):

  for i in initial_population : 
    logging.info(i.data ) 

  global reference_population
  global min_values
  global max_values

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

  if graph_objectives:
    features = {}
    for key in population[0].score.keys():
      features[key] = []
    if calc_igd:
      features['igd'] = []
  
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

    if graph_objectives:
      for key in population[0].score.keys():
        features[key].append(avg_decision(key,population))
      if calc_igd:
        features['igd'].append(igd(m, population))
  
  if graph_objectives:
    for key in features.keys():
      plotfeature(key, features[key])
  
  return population

def set_baseline(m, runs = 10, selector=Selector(Selector.bdom)):
  print("calculating baseline...")
  def set_maxmin(m, large_population):
    for key in large_population[0].score.keys():
      for obj in m.objs:
        if obj.name == key:
          obj.baseline_max = max(large_population,key = lambda x:x.score[key]).score[key]
          obj.baseline_min = min(large_population,key = lambda x:x.score[key]).score[key]
      

  adjLst = m.getWaypoints( coverage=0.2, renderNetwork=False ) 
  pop    = m.generatePaths( 50, adjLst, maxLen=25, showPaths=False ) 

  # large population
  best_solutions = []
  for _ in xrange(runs):
    best_solutions.extend(GA( m, pop, mutator=Mutator(), selector=selector, gens=20, popSize=50, render=False ) )
  
  set_maxmin(m, best_solutions)
  
  #downselect
  m.baseline_population = selector( m, best_solutions, 50 )

def avg_decision(dec, population):
  i = 0
  for p in population:
    i+=p.score[dec]
  return i/len(population)

def plotfeature(feature, performance):
  print("plotting objective bar graphs...")
  objects = ["gen{}".format(i) for i in xrange(len(performance))]
  y_pos = np.arange(len(objects))
  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects)
  plt.ylabel(feature)
  plt.title('Path scoring')
  plt.savefig('exp_1_{}_plot.png'.format(feature))
  plt.clf()


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

  gold = []
  step = []
  goal = []
  for _ in xrange( 50 ) : 
    adjLst = m.getWaypoints( coverage=0.03, renderNetwork=False ) 
    pop    = m.generatePaths( 50, adjLst, maxLen=25, showPaths=False ) 
    pop    = GA( m, pop, mutator=Mutator(), selector=Selector(Selector.cdom), gens=20, popSize=50, render=False, calc_igd=False, graph_objectives=False ) 

    gold.append( sum( [x.score["gold"] for x in pop] ) / len( pop ) )
    step.append( sum( [x.score["steps"] for x in pop] ) / len( pop ) )
    goal.append( sum( [x.score["goal"] for x in pop] ) / len( pop ) )

  print( gold ) 
  print( step ) 
  print( goal ) 

