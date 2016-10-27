from sa         import optimize as sa_optimize 
from maxwalksat import optimize as mws_optimize 

"""
results = []
for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [sa_optimize, mws_optimize]:
           results.append(optimizer(model())) 

for x in results : 
  pretty_print( x ) 

"""


