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

class Model():
    def __init__(self,name, decisions, objectives, constraints=[]):
        self.name = name
        self.decisions = decisions
        self.objectives = objectives
        self.constraints = constraints

    def ok(self):
        return all([c(self.decisions) for c in self.constraints])

    def generate_solution(self,retries = 500):
        for d in self.decisions:
            i = retries
            while(not d.isvalid()):
                if i < 0:
                    import sys
                    print("Couldn't find a valid solution in {} retries".format(retries))
                    sys.exit(0)
                d.generate()
                i-=1

    def e_val(self):
        for o in self.objectives:
            o.e_val(self.decisions)
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

schaffer.generate_solution()
osyczka.generate_solution()
kursawe.generate_solution()

print(schaffer.name,[d.value for d in schaffer.decisions],schaffer.e_val())
print(osyczka.name,[d.value for d in osyczka.decisions],osyczka.e_val())
print(kursawe.name,[d.value for d in kursawe.decisions],kursawe.e_val())

