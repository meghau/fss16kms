# All the imports
from __future__ import print_function, division
from math import *
import random
import sys
import matplotlib.pyplot as plt

# DONE 1: Enter youddr unity ID here 
__author__ = "gbtimmon"

class O:
    """
    Basic Class which
        - Helps dynamic updates
        - Pretty Prints
    """
    def __init__(self, **kwargs):
        self.has().update(**kwargs)
    def has(self):
        return self.__dict__
    def update(self, **kwargs):
        self.has().update(kwargs)
        return self
    def __repr__(self):
        show = [':%s %s' % (k, self.has()[k]) 
                for k in sorted(self.has().keys()) 
                if k[0] is not "_"]
        txt = ' '.join(show)
        if len(txt) > 60:
            show = map(lambda x: '\t' + x + '\n', show)
        return '{' + ' '.join(show) + '}'
    
print("Unity ID: ", __author__)

# Few Utility functions
def say(*lst):
    """
    Print whithout going to new line
    """
    print(*lst, end="")
    sys.stdout.flush()

def gt(a, b): return a > b

def lt(a, b): return a < b

def shuffle(lst):
    """
    Shuffle a list
    """
    random.shuffle(lst)
    return lst

class Decision(O):
    """
    Class indicating Decision of a problem
    """
    def __init__(self, name, low, high):
        """
        @param name: Name of the decision
        @param low: minimum value
        @param high: maximum value
        """
        O.__init__(self, name=name, low=low, high=high)
   
    def __call__( self, decimals=2 ) : 
        return round( random.uniform( self.low, self.high), decimals ) 
        
class Objective(O):
    """
    Class indicating Objective of a problem
    """
    def __init__(self, name, do_minimize=True):
        """
        @param name: Name of the objective
        @param do_minimize: Flag indicating if objective has to be minimized or maximized
        """
        O.__init__(self, name=name, do_minimize=do_minimize)


class Point(O):
    """
    Represents a member of the population
    """
    def __init__(self, decisions):
        O.__init__(self)
        self.decisions = decisions
        self.objectives = None

    def __hash__(self):
        return hash(tuple(self.decisions))
    
    def __eq__(self, other):
        return self.decisions == other.decisions
    
    def clone(self):
        new = Point(self.decisions)
        new.objectives = self.objectives
        return new

class Problem(O):
    """
    Class representing the cone problem.
    """
    def __init__(self):
        O.__init__(self)
        self.decisions  = [ Decision( "h", 0, 20), Decision("r", 0,10)  ]
        self.objectives = [ Objective("S",True),   Objective("T", True) ]
        
    @staticmethod
    def evaluate(point):
        [r, h] = point.decisions
        s = ( r**2 + h**2 ) ** 0.5
        B = pi * r * r
        S = pi * r * s
        T = B + S
        point.objectives = (S, T)
        return point.objectives
    
    @staticmethod
    def is_valid(point):
        [r, h] = point.decisions
        V = (pi / 3) * r * r * h
        return ( V > 200 )
    
    def generate_one(self):
        return Point( [ x() for x in self.decisions ]  )


def populate(problem, size):
    population = [ problem.generate_one() for x in range(size) ]
    return population
        
def crossover(mom, dad):
    decisions = [ mom.decisions[x] if x % 2 == 0 else dad.decisions[x] for x in range(len(mom.decisions)) ]
    return Point( decisions )

def mutate(problem, point, mutation_rate=0.01):

    for x in range( len( point.decisions ) ) : 
        if( random.random() < mutation_rate ) :
            point.decisions[x] = problem.decisions[x]()

    return point

def bdom(problem, one, two):
    """
    Return if one dominates two
    """
    a = problem.evaluate(one)
    b = problem.evaluate(two)
    
    oneSmaller    = False
    allSmallerOrE = True

    for (x,y) in zip(a,b) : 
        if( x > y )  : allSmallerOrE = False
        if( x < y )  : oneSmaller    = True

    return (oneSmaller and allSmallerOrE)

def fitness(problem, population, point):
    return sum( [ 0 if bdom(problem, point, x ) else 1 for x in population ] )
   

def elitism(problem, population, retain_size):
    fits = [ fitness( problem, population, x) for x in population ]
    population = [ x for (y, x) in sorted(zip(fits, population), key=lambda p:p[0])]
    return population[:retain_size]

def ga(pop_size = 100, gens = 250):
    problem = Problem()
    population = populate(problem, pop_size)
    [problem.evaluate(point) for point in population]
    initial_population = [point.clone() for point in population]
    gen = 0 
    while gen < gens:
        say(".")
        children = []
        for _ in range(pop_size):
            mom = random.choice(population)
            dad = random.choice(population)
            while (mom == dad):
                dad = random.choice(population)
            child = mutate(problem, crossover(mom, dad))
            if problem.is_valid(child) and child not in population+children:
                children.append(child)
        population += children
        population = elitism(problem, population, pop_size)
        gen += 1
    print("")
    return initial_population, population

def plot_pareto(initial, final):
    initial_objs = [point.objectives for point in initial]
    final_objs = [point.objectives for point in final]
    initial_x = [i[0] for i in initial_objs]
    initial_y = [i[1] for i in initial_objs]
    final_x = [i[0] for i in final_objs]
    final_y = [i[1] for i in final_objs]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(final_x, final_y, color='r', marker='o', label='final')
    ax1.scatter(initial_x, initial_y, color='b', marker='+', label='initial')
    plt.title("Scatter Plot between initial and final population of GA")
    plt.ylabel("Total Surface Area(T)")
    plt.xlabel("Curved Surface Area(S)")
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.175), ncol=2)
    plt.show()
    
initial, final = ga()
plot_pareto(initial, final)
