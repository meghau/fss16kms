from __future__ import division,print_function
import random as r
r.seed(1000)

class Decision():
    def __init__(self, name, minbound, maxbound):
        self.name = name
        self.maxbound = maxbound
        self.minbound = minbound
        self.value = None

    def isvalid(self):
        return self.minbound <= self.value <= self.maxbound

    def generate(self):
        import random as r
        self.value = r.uniform(self.minbound, self.maxbound)

class Objective():
    def __init__(self, name, formula_func):
        self.name = name
        self.value = None
        self.formula_func = formula_func

    def e_val(self, solution):
        self.value = self.formula_func(solution)

class Solution():
    def __init__(self, decisions):
        self.decisions = decisions 
        self.objectives = None
        
    def __hash__(self):
        return hash(tuple(self.decisions))
    
    def __eq__(self, other):
        return self.decisions == other.decisions
    
    def clone(self):
        new = Solution(self.decisions[:])
        #new.objectives = self.objectives[:]
        return new

class Model():
    def __init__(self,name, decisions, objectives, constraints=[]):
        self.name = name
        self.decisions = decisions
        self.objectives = objectives
        self.constraints = constraints

    def ok(self,solution):
        return all([c(solution.decisions) for c in self.constraints])

    def generate_solution(self,retries = 500):
        for d in self.decisions:
            d.generate()
        solution = Solution(self.decisions)
        i = retries - 1    
        
        while ( not self.ok(solution) ):
            if i < 0:
                #import sys
                print("Couldn't find a valid solution for {} in {} retries".format(self.name,retries))
                break
                #sys.exit(0)

            for d in self.decisions:
                d.generate()
            solution = Solution(self.decisions)
            i-=1
            
        return solution

    #check - this and above
    def e_val(self, solution):
        for o in self.objectives:
            o.e_val(solution.decisions)
        return sum([o.value for o in self.objectives])

import math

schaffer = Model("Schaffer", 
                [ Decision("x",-10**5,10**5) ],
                [ Objective("f1", lambda x: x[0].value**2),  
                  Objective("f2", lambda x: (x[0].value-2)**2) ],
            )

osyczka = Model("Osyczka",
                [ Decision("x1",0,10),
                  Decision("x2",0,10),
                  Decision("x3",1,5),
                  Decision("x4",1,5),
                  Decision("x5",0,6),
                  Decision("x6",0,10) ],
                [ Objective("f1", lambda x: -1*(25*(x[0].value-2)**2 + (x[1].value-2)**2 + ((x[2].value-1)**2)*((x[3].value-4)**2) + (x[4].value - 1)**2)),
                  Objective("f2", lambda x: sum([i.value**2 for i in x])) ],
                [ lambda x: 0 <= (x[0].value + x[1].value - 2),
                  lambda x: 0 <= (6 - x[0].value - x[1].value),
                  lambda x: 0 <= (2 - x[1].value + x[0].value),
                  lambda x: 0 <= (2 - x[0].value + 3*x[1].value),
                  lambda x: 0 <= (4 - (x[0].value - 3)**2 - x[1].value),  
                  lambda x: 0 <= ((x[0].value - 3)**3 + x[1].value - 4)
                ]
            )

kursawe = Model("Kursawe",
                [ Decision("x1",-5,5),
                  Decision("x2",-5,5),
                  Decision("x3",-5,5) ],
                [ Objective("f1", lambda dec: sum([(-10)*(math.e**(-0.2*((dec[i].value**2 + dec[i+1].value**2)**0.5))) for i in [0,1]])),
                  Objective("f2", lambda dec: sum([abs(x.value)**0.8 + 5*math.sin(x.value**3) for x in dec])) ],
            )    

'''schaffer.generate_solution()
osyczka.generate_solution()
kursawe.generate_solution()

print(schaffer.name,[d.value for d in schaffer.decisions],schaffer.e_val())
print(osyczka.name,[d.value for d in osyczka.decisions],osyczka.e_val())
print(kursawe.name,[d.value for d in kursawe.decisions],kursawe.e_val())'''

def sa(model):
  def Probability(old,new, t):
    from math import e
    return e**((old-new)/(t+10e-7))
  
  s = model.generate_solution() 
  e = model.e_val(s)
  sb = s.clone()
  eb = e
  k = 0
  kmax = 2000
  emax = 1e-7
  print ("\n, %04d, :%3.5f " %(k,eb),end="")
  while( k < kmax and e > emax):
    sn = model.generate_solution() 
    en = model.e_val(sn)
    if(en < eb):
      sb = sn.clone()
      eb = en
      print("!",end="")
    
    if(en < e):
      s = sn.clone() 
      e = en
      print("+",end="")                        
    
    elif(Probability(e, en, k/kmax) < r.random()):
      s = sn.clone()
      e = en
      print("?",end="")
    
    print(".",end="")
    k = k + 1   
    
    if k % 25 == 0: 
      print ("\n, %04d, :%3.5f " % (k,eb), end="")
  return sb
  
sa(schaffer)
