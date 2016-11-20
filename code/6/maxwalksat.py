from __future__ import division, print_function
import random
from model  import Model
from O      import o 
import copy

def optimize( model ) : 
    return maxwalksat( model, max_tries=15, max_changes=50 ).go()

class maxwalksat(o) : 
    def __init__(self, model, max_tries, max_changes): 
        super( o, self ).__init__()
        self.model      = model
        self.log        = ""
        self.line_size  = 25
        self.maxchanges = max_changes
        self.maxtries = max_tries
        self.p_of_jump = 0.5
        self.threshold = None
        self.best_solution = None

    def mutate(self, solution):
        """
        function to generate a mutated solution which consists of mutated decisions.
        each decision is mutated randomly within +-10% range of its original value
        the range is adjusted to be within the variable bounds
        the percent is defined in variable p(=0.1).
        we generate the new bounds and call generate_solution function which also checks the constraints
        """
        p = 0.1
        decisions_copy = copy.deepcopy(self.model.decisions)
        for i,d in enumerate(self.model.decisions):
            d.minbound = min(solution.decisions[i]-p*d.minbound, d.minbound)
            d.maxbound = max(solution.decisions[i]+p*d.maxbound, d.maxbound)
            
        s = self.model.generate_solution()
        self.model.decisions = decisions_copy
        return s
     
    def go(self):
        """
        There are 3 main steps:
            [1] generate a random solution, check if its better than best, if yes it is the new best
            [2] LocalSearch - one of following:
                + at probability p_of_jump assign random values to a decision pair(chosen at random) (here only a part of the original solution is changed)
                + at probability 1-p_of_jump mutate the solution to within +-10% of its original value by calling mutate function (here whole solution is changed)
            [3] if the solution is better than best, it is the new best

        step [1] - repeated maxtries no of times
        step [2] - repeated maxchanges no of times, for each step[1]

        at each random generation print ?
        if a better solution is found print +
        if global best is found print ! else print .

        best_solution is initiated as best of 5 random runs
        threshold is initiated as worst of 5 random runs
        """
        runs = []
        for _ in xrange(5):
            solution = self.model.generate_solution()
            self.model.eval(solution)
            runs.append(sum(solution.objectives))
        
        self.best_solution, self.threshold = max(runs), min(runs)
        for i in xrange(self.maxtries):
            solution = self.model.generate_solution()
            print("?", end="")
            for j in xrange(self.maxchanges):
                self.model.eval(solution)
                s = sum(solution.objectives)
                if s < self.threshold and s < self.best_solution:
                    self.best_solution = s
                    print("!", end="")
                else:
                    print(".", end="")
            
                if(self.p_of_jump < random.random()):
                    #local search i.e. mutate in one dimension
                    #select dimension at random
                    index = random.randint(0,len(self.model.decisions)-1)
                    solution.generate_decision(index)

                else:
                    mutant = self.mutate(solution)
                    self.model.eval(mutant)
                    m = sum(mutant.objectives)
                    if m > s:
                        print("+", end="")
                    solution = mutant
            print("\n", end="")
        return self