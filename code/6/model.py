from __future__ import division,print_function
import math
from O  import o 
import random as r

class Decision():

    """
    Decision object holds the metadata of how to make a decision
    I changed it so it does not hold the value of that decision since 
    that made the memory model very confusing
    """

    def __init__(self, name, minbound, maxbound):
        self.name = name
        self.maxbound = maxbound
        self.minbound = minbound
 
    def generate(self):
        return r.uniform(self.minbound, self.maxbound)

def gt   ( a, b ) : return a > b
def lt   ( a, b ) : return a < b
def zero ( a, b ) : return math.abs(a) < math.abs(b)

class Objective():

    """
    Object holds meta data for how to generate an objective
    value and how to judge the fitness of one objective against another
    *Objective does not return a 'score' just a value - you have to define 
    the better 
    """

    def __init__(self, name, formula, better=gt ):
        self.name    = name
        self.better  = better
        self.formula = formula

    def eval(self, solution):
        return self.formula(solution)

class Solution():

    """
    I made solution randomly genertate on creation. 
    less code makes me happy 
    """
    def __init__(self, decisions):
        self.decisions  = [ d.generate() for d in decisions ]
        self.objectives = None

    def __getitem__( self, x ) : 
        return self.decisions[x] 

    def eval( self, objectives ) : 
        self.objectives = [ o.eval(self) for o in objectives ]
        return self #so i can chain s = Model.guess().eval() if I want.
        
    def __eq__(self, other):
        return self.decisions == other.decisions
    
    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return str([self.decisions, self.objectives])

class Constraint() :
    def __init__(self, name, lam ) : self.name, self.lam = name, lam
    def __call__(self, *arg) : return self.lam( *arg ) 

class Model():
 
    """
    Default models. Defined in lists below. 
    """
    
    @staticmethod
    def schaffer ( ) : return Model( *_schaffer )

    @staticmethod
    def osyczka ( )  : return Model( *_osyczka  )

    @staticmethod
    def kursawe ( )  : return Model( *_kursawe  )
    
    def __init__(self,name, *decl, **kwargs):
        self.name        = name
        self.decisions   = [ x for x in decl if isinstance( x, Decision   ) ]
        self.objectives  = [ x for x in decl if isinstance( x, Objective  ) ]
        self.constraints = [ x for x in decl if isinstance( x, Constraint ) ]

    def ok(self,solution):

        if self.constraints : 
            return all([c(solution.decisions) for c in self.constraints])
        else :
            return True

    def guess( self, retries=500) : return self.generate_solution(retries=retries)
    def generate_solution(self,retries = 500):
        i = retries
        while( i > 0 ) : 
           s = Solution( self.decisions )
           if( self.ok( s ) ): return s
           i -= 1        

        raise Exception("Failed to generate valid solution in %d trys. Giving up."%(retries) ) 

    def eval( self, solution ) : 
        if solution.objectives == None : 
            solution.eval( self.objectives )
        return solution.objectives 

    def __str__( self ) : 
        return ( 
             self.__class__.__name__ + " " + self.name 
             + " : Decisions " + str([ x.name for x in self.decisions ])
             + ", Objectives " + str([ x.name for x in self.objectives ])
             + ", Constraints " + str([ x.name for x in self.constraints ])
        )


_schaffer = [
    "Schaffer", 
    Decision("x",-10**5,10**5),
    Objective("f1", lambda x: x[0]**2, better=lt),  
    Objective("f2", lambda x: (x[0]-2)**2, better=lt),
]

_osyczka = [
    "Osyczka",
    Decision("x1",0,10),
    Decision("x2",0,10),
    Decision("x3",1,5),
    Decision("x4",0,6),
    Decision("x5",1,5),
    Decision("x6",0,10),
    Objective("f1", lambda x: -1*(25*(x[0]-2)**2 + (x[1]-2)**2 + ((x[2]-1)**2)*((x[3]-4)**2) + (x[4] - 1)**2), better=lt),
    Objective("f2", lambda x: sum([i**2 for i in x]), better=lt),
    Constraint( "c1", lambda x: 0 <= (x[0] + x[1] - 2) ),
    Constraint( "c2", lambda x: 0 <= (6 - x[0] - x[1]) ),
    Constraint( "c3", lambda x: 0 <= (2 - x[1] + x[0]) ), 
    Constraint( "c4", lambda x: 0 <= (2 - x[0] + 3*x[1]) ),
    Constraint( "c5", lambda x: 0 <= (4 - (x[2] - 3)**2 - x[3]) ),  
    Constraint( "c6", lambda x: 0 <= ((x[4] - 3)**3 + x[5] - 4) ) 
]

_kursawe = [
    "Kursawe",
    Decision("x1",-5,5),
    Decision("x2",-5,5),
    Decision("x3",-5,5),
    Objective("f1", lambda dec: sum([(-10)*(math.e**(-0.2*((dec[i]**2 + dec[i+1]**2)**0.5))) for i in [0,1]])),
    Objective("f2", lambda dec: sum([abs(x)**0.8 + 5*math.sin(x)**3 for x in dec]))
]
