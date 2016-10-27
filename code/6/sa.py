#LET s = s0
#FOR k = 0 through kmax
#   T<- temperature( k / kmax )
#   Pick a random neighboor snew <- neighbor(s)
#   if( P(E(s), E(snew), T) >= random.random() : move
#      s <- snew
#Output final state

from __future__ import division, print_function
from sys    import float_info, stdout, argv
from math   import e
from random import Random


def sa( model ) : 

    # do stuff
    return o() 

def schaffer( x ) : 
    """
    Schaffer function default, our class will allow us to pass in another function 
    if desired -- I tried to generally make it work with more than 2 outputs but its 
    not really tested nor am I sure itll work yet. 
    """
    return (x**2, (x-2)**2)

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

class simulated_annealer() : 
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

    def __init__( 
           self, 
           metric       = schaffer,    
           output       = True,         
           drunk_metric = drunkeness,    
           max_iter     = 5000,           
           min_energy   = 1e-6,           
           valid_range  = (-10e6, 10e6),
           seed         = None,
           bline_iter   = 200
    ): 

        self.output     = output
        self.random     = Random()            # seeded random. 
        self.metric     = metric              # Function for determining energy
        self.isDrunk    = drunk_metric        # Function for determining if I should go worse
        self.max_iter   = max_iter            # max number of iterations before I give up
        self.min_energy = min_energy          # target energy
        self.range      = valid_range         # valid range of values to search for solution
        self.iter       = 0                   # current iter
        self.terminated = False               # is terminated
        self.omin       = 0
        self.omax       = 0 
        self.line_size  = 25

        if( seed is not None ) :
            self.random.seed( int(seed) )

        for _ in xrange( bline_iter ) : 
            x = sum( self.metric( self.random.randint( *self.range ) ) ) 
            self.omin = min( self.omin, x )
            self.omax = max( self.omax, x )       

        self.cur_state  = self.random.randint( *self.range ) # initial state
        self.cur_energy = self.energy(self.cur_state)        # initial energy
        self.bst_state  = self.cur_state                     # initial best state
        self.bst_energy = self.cur_energy                    # initial best energy

    def stop( self ) : 
        self.terminated = True

    def say(self, *lst):
        if( self.output == False ) : return
        print(*lst, end="")
        stdout.flush()

    def energy( self, x ) : 
        return (
            float(sum(self.metric(x)) - self.omin) 
            / float(self.omax - self.omin)
        )

    def step( self ) : 
        if self.terminated : 
            raise ValueError("annealer has terminated")

        new_state  = self.random.randint( *self.range )
        new_energy = self.energy( new_state )

        if( new_energy < self.bst_energy ):
            self.bst_state  = new_state
            self.bst_energy = new_energy
            self.say("!")

        if self.bst_energy < self.min_energy : 
            self.stop()

        if( new_energy < self.cur_energy ) : 
            self.cur_state  = new_state
            self.cur_energy = new_energy
            self.say("+")

        elif( 
            self.isDrunk( self.cur_energy, new_energy, 
                self.iter, self.max_iter, self.random )
        ) :
            self.cur_state  = new_state
            self.cur_energy = new_energy
            self.say("?")

        self.say(".")
       
        if( self.iter % self.line_size == 0 ) :
            self.say( "\n[%04d] %12.10f : " % ( self.iter, self.bst_energy ) ) 

        self.iter += 1

        if self.iter > self.max_iter : 
            self.stop()

    def go( self ) :
        if self.terminated :
            raise ValueError("annealer has terminated")

        self.say("\n[%04d] %12.10f : " % ( self.iter, self.bst_energy ))
        while ( not self.terminated ) :
            self.step()
              
        self.say("\n")
  
        return self

if __name__ == '__main__' :
    print(argv)
    if( len(argv) > 1 ) : 
        sa = simulated_annealer( seed=argv[1], min_energy=1e-9, max_iter=9000 ).go()
    else :
        sa = simulated_annealer( min_energy=1e-7, max_iter=2000 ).go()
       
    print()
    print("e : ", sa.bst_energy)
    print("s : ", sa.bst_state)
    print("max iter : ", sa.max_iter)
    print("min engy : ", sa.min_energy)
    print("iters    : ", sa.iter)

   
