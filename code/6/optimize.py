from __future__ import print_function
from O          import o 
from model      import Model
from sa         import optimize as sa_optimize 
from maxwalksat	import optimize as mws_optimize

def pretty_print(r) :
   for k,v in r : 
      if( k.startswith("_") ) :
         continue
      print( " %25s : %s"%(k,v) ) 
    
results = []
for model in [ Model.schaffer(), Model.osyczka(), Model.kursawe() ]:
    for optimizer in [sa_optimize, mws_optimize]:
        res = optimizer(model)
        pretty_print(res) 