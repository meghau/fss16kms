from __future__ import division, print_function
from random import randint
import sys

if len(sys.argv) != 2:
    print("Usage: python birthday_paradox.py <number-of-trials>")
    exit(1)

def has_duplicates(lst):
    count = { }
    for e in lst:
        if e in count:
            return True
        count[e] = 1
    return False
    
def generate_birthday_list():
    bday_list = [randint(1,365) for i in xrange(23)]
    return bday_list

def perform_experiment():
    return has_duplicates(generate_birthday_list())
    
def calculate_probabilty():
    count = 0
    for x in xrange(num_trials):
        if perform_experiment():
            count += 1
    return count/num_trials

try:
    num_trials = int(sys.argv[1])
    print("Number of trials: %d" % num_trials)
    print("Probability: %f" % calculate_probabilty())
except ValueError as e:
    print("The argument <number-of-trials> is not a valid integer.")