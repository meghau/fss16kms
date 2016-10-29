from O          import o 
from model      import Model
from sa         import optimize as sa_optimize 


def pretty_print( O ) :
   for k,v in O : 
      if( k.startswith("_") ) :
         continue
      print( " %25s : %s"%(k,v) ) 
    
results = []
for model in [ Model.schaffer(), Model.osyczka(), Model.kursawe() ]:
    for optimizer in [sa_optimize]:
        res = optimizer(model)
        pretty_print( 


