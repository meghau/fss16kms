"""
MaxWalkSat optimizer for Osyczka2 model.

The Osyczka model has 6 decisions and 2 objectives. 
There are 6 constraints that have to be checked. Each constraints takes 2 decisions as input.
Looking at the 6 constraints, decisions can be abstracted in pairs of 2.
if decisions and constraints are 1D sequence, and "->" indicates "has to satisfy"
decisions(1,2) -> constraints(1,2,3,4)
decisions(2,3) -> constraints(5)
decisions(4,5) -> constraints(6)

"""
from __future__ import division, print_function
import random

def generate_pair(bounds_lst,constraint_func,retries=500):
    """
    function to generate a random pair of decisions, float in value, which satisfy the constraint_func provided
    bounds_lst is a list of 2 (min,max) bounds for each decision
    constraint_func accepts a sequence of 2 values and returns a boolean
    retries is set to 500 by default, if it can't find a valid pair then returns False
    """
    if(retries<0):
        return False
    b1,b2 = bounds_lst
    val1 = random.uniform(b1[0],b1[1])
    val2 = random.uniform(b2[0],b2[1])
    if not constraint_func((val1,val2)):
        return generate_pair(bounds_lst,constraint_func,retries-1)
    return [val1,val2]

def generate_solution(bounds):
    """
    function to generate a random valid solution consisting of six decisions.
    solution is generated in pairs by calling generate_pair function
    bounds is a list argument consisting of 6 bounds of the 6 decisions
    """
    solution = []
    for i in range(3):
        solution.extend(generate_pair([bounds[i*2],bounds[i*2+1]],constraints[i]))
        
    assert len(solution)==6
    return solution

def mutate(x):
    """
    function to generate a mutated solution which consists of mutated decisions.
    each decision is mutated randomly within +-10% range of its original value
    the range is adjusted to be within the variable bounds
    the percent is defined in variable p(=0.1).
    we generate the new bounds and call generate_solution function which also checks the constraints
    """
    global bounds
    p = 0.1
    new_bounds = []
    for i in xrange(6):
        mn = min(x[i]-p*bounds[i][0], bounds[i][0])
        mx = max(x[i]+p*bounds[i][1], bounds[i][1])
        bound = (mn,mx)
        new_bounds.append(bound)
    
    return generate_solution(new_bounds)

def energy(x):
    """
    Input is a valid solution -> list of 6 decisions.
    Calculate the 2 energies associated with Osyczka model
    f1 is a negative value
    f2 is a positive value
    """
    
    f1 = -1*(
            25*(x[0]-2)**2 + 
            (x[1]-2)**2 +
            ((x[2]-1)**2)*((x[3]-4)**2) +
            (x[4] - 1)**2
            )
    f2 = sum([i**2 for i in x])
    return f1,f2

def score(x):
    """
    Input is f1,f2 returned from energy(x)
    Return the score which is f1+f2
    Since here we are minimizing the model, we would need to maximize
    f1 and minimize f2. 
    Smaller score is better.
    """
    return x[0]+x[1]
 
def maxwalksat(maxtries=15,maxchanges=50):
    """
    Return the minimum score for the Osyczka model.
    There are 3 main steps:
        [1] generate a random solution, check if its better than best, if yes it is the new best
        [2] LocalSearch - one of following:
            + at probability p assign random values to a decision pair(chosen at random) (here only a part of the original solution is changed)
            + at probability 1-p mutate the solution to within +-10% of its original value by calling mutate function (here whole solution is changed)
        [3] if the solution is better than best, it is the new best

    step [1] - repeated maxtries no of times
    step [2] - repeated maxchanges no of times, for each step[1]

    at each random generation print ?
    if a better solution is found print +
    if global best is found print ! else print .

    best_solution is initiated as any random solution
    """
    threshold = -100
    best_solution = score(energy(generate_solution(bounds)))
    p=0.5
    for i in xrange(maxtries):
        solution = generate_solution(bounds)
        print("?",end="")
        for j in xrange(maxchanges):
            s = score(energy(solution))
            if s < threshold and s < best_solution:
                best_solution = s
                print("!",end="")
            else:
                print(".",end="")
        
            c = random.randint(0,2)
            if(p < random.random()):
                pair = generate_pair([bounds[c*2],bounds[c*2+1]],constraints[c])
                solution[2*c] = pair[0]
                solution[2*c+1] = pair[1]
            else:
                mutant = mutate(solution)
                if score(mutant)>score(solution):
                    print("+",end="")
                solution = mutant
        print()
    return best_solution

#the original bounds for the six decisions
bounds = (
            (0,10),
            (0,10),
            (1,5),
            (1,5),
            (0,6),
            (0,10)
        )

#the original constraints for the six decisions, stored as functions that accept a sequence of 2 decisions
#and return True if they satisfy all the constraints associated with the pair
# constraints[0] is associated with decision 0,1
# constraints[1] is associated with decision 3,4
# constraints[2] is associated with decision 4,5

constraints = [
    lambda x: all([ 0 <= (x[0] + x[1] - 2),
                    0 <= (6 - x[0] - x[1]),
                    0 <= (2 - x[1] + x[0]),
                    0 <= (2 - x[0] + 3*x[1])]),
    
    lambda x: 0 <= (4 - (x[0] - 3)**2 - x[1]),  
    lambda x: 0 <= ((x[0] - 3)**3 + x[1] - 4)
    ]

print(maxwalksat())