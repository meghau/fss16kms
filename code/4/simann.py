from __future__ import division,print_function
import random as r
mn = mx = r.randint((-10)**5,10**5)

def Probability(old,new, t):
  from math import e
  return e**((old-new)/(t+0.00001))

def sim_anneal(kmax, emax):
  s = r.randint((-10)**5,10**5) 
  e = energy(s)                                           # Initial state, energy.
  sb = s 
  eb = e                                                  # Initial "best" solution
  k = 0                                                   # Energy evaluation count.
  print ("\n, %04d, :%3.5f " %(k,eb),end="")
  while( k < kmax and e > emax):                          # While time remains & not good enough:
    sn = r.randint((-10)**5,10**5)                        #   Pick some neighbor.
    en = energy(sn)                                       #   Compute its energy.
    
    if(en < eb):                                          #   Is this a new best?
      sb = sn 
      eb = en                                             #     Yes, save it.
      print("!",end="")
    
    if(en < e):                                           # Should we jump to better?
      s = sn 
      e = en                                              #    Yes!
      print("+",end="")                        
    
    elif(Probability(e, en, k/kmax) < r.random()):        # Should we jump to worse?
      s = sn
      e = en                                              #    Yes, change state.
      print("?",end="")
    
    print(".",end="")
    k = k + 1                                             #   One more evaluation done    
    
    if k % 25 == 0: 
      print ("\n, %04d, :%3.5f " % (k,eb), end="")
  return sb

def schaffer(x):
  return x**2,(x-2)**2

def energy(x):
  global mn,mx
  f1,f2 = schaffer(x)
  f = f1+f2
  return (f-mn)/(mx-mn)

def baseline():
  global mn,mx 
  for i in xrange(100):
    f1,f2 = schaffer(r.randint((-10)**5,10**5))
    x = f1+f2
    if x>mx:
      mx = x
    if x<mn:
      mn = x

if __name__ == '__main__':
  baseline()
  sim_anneal(500,0.000001)
