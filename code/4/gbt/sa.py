#LET s = s0
#FOR k = 0 through kmax
#   T<- temperature( k / kmax )
#   Pick a random neighboor snew <- neighbor(s)
#   if( P(E(s), E(snew), T) >= random.random() : move
#      s <- snew
#Output final state

from __future__ import division
from sys    import float_info 
from math   import e
from random import Random

def schaffer( x ) : 
    return (x**2, (x-2)**2)

def drunkeness( old, new, k, kmax, rnd) : 
    top  = old - new
    bot  = k / kmax
    p    = e**(top/bot)
    rand = rnd.random()
    return p < rand 

class simulated_annealer() : 
    def __init__( 
           self, 
           metric       = schaffer, 
           drunk_metric = drunkeness,
           max_iter     = 5000, 
           min_energy   = 10e-6,
           valid_range  = (-10e6, 10e6),
           seed         = 1288,
           bline_iter   = 200
    ): 

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

        self.random.seed(seed)

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

    def energy( self, x ) : 
        return (
            float(sum(self.metric(x)) - self.omin) 
            / float(self.omax - self.omin)
        )

    def step( self ) : 
        if self.terminated : 
            raise ValueError("annealer has terminated")

        if self.iter > self.max_iter : 
            self.stop()

        if self.cur_energy < self.min_energy : 
            self.stop()
       
        new_state  = self.random.randint( *self.range )
        new_energy = self.energy( new_state )

        if( new_energy < self.bst_energy ):
            self.bst_state  = new_state
            self.bst_energy = new_energy
            print "!",

        if( new_energy < self.cur_energy ) : 
            self.cur_state  = new_state
            self.cur_energy = new_energy
            print "+",

        elif( 
            self.isDrunk( self.cur_energy, new_energy, 
                self.iter, self.max_iter, self.random )
        ) :
            self.cur_state  = new_state
            self.cur_energy = new_energy
            print "?",

        print ".",
       
        self.iter += 1

        if( self.iter % self.line_size == 0 ) :
            print "\n[%04d] %12.10f : " % ( self.iter, self.bst_energy ) , 

    def go( self ) :
        if self.terminated :
            raise ValueError("annealer has terminated")

        print "\n[%04d] %12.10f : " % ( self.iter, self.bst_energy ),
        while ( not self.terminated ) :
            self.step()
              
        print ""
  
        return self

if __name__ == '__main__' :
    sa = simulated_annealer().go()
    print ""          
    print "e : " + str(sa.bst_energy)
    print "s : " + str(sa.bst_state)


