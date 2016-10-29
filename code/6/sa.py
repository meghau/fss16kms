#LET s = s0
#FOR k = 0 through kmax
#   T<- temperature( k / kmax )
#   Pick a random neighboor snew <- neighbor(s)
#   if( P(E(s), E(snew), T) >= random.random() : move
#      s <- snew
#Output final state

from __future__ import division, print_function
from sys    import float_info, stdout, argv, exit
from math   import e
from random import Random
from model  import Model
from O      import o 
from Num    import Num


def optimize( model ) : 
    return simulated_annealer( model, min_energy=1e-7, max_iter=2000 ).go()

def drunkeness( old, new, k, kmax, rnd) : 
    """
    Like the schaffer function I can pass in custom drunkeness functions. 
    It assumes the inputs : 

       @old  : the energy I was 
       @new  : the energy Im moving to 
       @k    : the current iteration
       @kmax : the max iteration 
    """
    top  = old - new
    bot  = k / kmax
    p    = e**(top/(bot + 10e-7))
    rand = rnd.random()
    return p < rand 

class simulated_annealer(o) : 
    """
    This class is will only minimize which really needs to be fixed if it is to be general.
    For the sake of this assignment it is enough, so well just leave it for now. 

    Generally you can work with the class like this : 

    >  sa = simulated_annealer( <params> ) 
      
    And step through manually allowing you to control reporting or take intervention 

    >  while( not sa.terminated ) : 
    >      pass

    Or just run till the passed in stopping criteria are met. 

    >  sa.go()
    
    """

    def energy( self, model, state ) : 
        s = 0 
        for obj, obj_value, num in zip(model.objectives, state.objectives, self._bline_data) : 
            if( obj.better( 1,2) ):
                s += ( obj_value - num.min ) / ( num.max - num.min )
            else :
                s += ( num.max - obj_value ) / ( num.max - num.min )
       
        return s / len( state.objectives ) 

    def __init__( 
           self, 
           model,
           drunk_metric = drunkeness,    
           max_iter     = 5000,           
           min_energy   = 1e-6,           
           bline_iter   = 5000,
           seed         = None
    ): 

        super( o, self ).__init__()
        self.model      = model
        self._isDrunk   = drunk_metric        # Function for determining if I should go worse
        self._seed       = seed
        self.max_iter   = max_iter            # max number of iterations before I give up
        self._iter      = 0                   # current iter
        self._term      = False               # is terminated
        self.log        = ""
        self.line_size  = 25
        self._random    = Random()

        if( seed is not None ) :
            self._random.seed( int(seed) )

        self._bline_data = [Num() for _ in range(len(model.objectives))]
        for _ in xrange( bline_iter ) : 
            s = model.guess()
            model.eval( s ) 
            for x,y in zip( s.objectives, self._bline_data) : y.add(x)

        self.cur_state  = model.guess()
        model.eval( self.cur_state )
        self.cur_energy = self.energy(model, self.cur_state)        # initial energy
        self.bst_state  = self.cur_state                     # initial best state
        self.bst_energy = self.cur_energy                    # initial best energy

    def stop( self ) : 
        self._term = True

    def say(self, st):
        self.log += st

    def step( self ) : 
        if self._term : 
            raise ValueError("annealer has terminated")

        new_state  = self.model.guess()
        self.model.eval( new_state ) 
        new_energy = self.energy( self.model, new_state ) 

        if( new_energy < self.bst_energy ):
            self.bst_state  = new_state
            self.bst_energy = new_energy
            self.say("!")

        if( new_energy < self.cur_energy ) : 
            self.cur_state  = new_state
            self.cur_energy = new_energy
            self.say("+")

        elif( 
            self._isDrunk( self.cur_energy, new_energy, 
                self._iter, self.max_iter, self._random )
        ) :
            self.cur_state  = new_state
            self.cur_energy = new_energy
            self.say("?")

        self.say(".")
       
        if( self._iter % self.line_size == 0 ) :
            self.say( "\n[%04d] %12.10f : " % ( self._iter, self.bst_energy ) ) 

        self._iter += 1

        if self._iter > self.max_iter : 
            self.stop()

    def go( self ) :
        if self._term :
            raise ValueError("annealer has terminated")

        self.say("\n[%04d] %12.10f : " % ( self._iter, self.bst_energy ))
        while ( not self._term ) :
            self.step()
              
        self.say("\n")
  
        return self

if __name__ == '__main__' :
    
    m = Model.schaffer()
    
    if len(argv) ==  1 :
        sa = simulated_annealer( m, min_energy=1e-7, max_iter=2000 ).go()
    else : 
        sa = simulated_annealer( m, min_energy=1e-7, max_iter=2000, seed=int(argv[1]) ).go()
