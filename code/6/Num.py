from __future__ import division
import sys
from math import *
class Num:

  def __init__( i ) :
    i.mu      = 0
    i.n       = 0
    i.m2      = 0
    i.max     = -sys.maxint - 1
    i.min     = sys.maxint

  def __str__( i ) : 
    return "NUM mu:%s n:%s m2:%s max:%s min:%s" %( str(i.mu), str(i.n), str(i.m2), str(i.max), str(i.min))

  def add( i, x):
    x = float(x)

    i.n += 1
    i.max = max( i.max, x )
    i.min = min( i.min, x )

    delta    = x - i.mu
    i.mu  += delta/i.n
    i.m2  += delta*(x - i.mu)
    return x 

  def norm( i, x ) :

    denom = i.max - i.min
    if( denom == 0 ) : return 0

    print( x, i.min, denom , 1234567 )
    norm = (x - i.min) / denom
    return norm

    
  def dist( i, a, b ) : 
    return abs(i.norm(b) - i.norm(a))

  def furthest ( i, x ) :
    return i.max if x <(i.max-i.min)/2 else i.min

  def sd( i ):
    return 10e-50 if i.n <= 1 else (i.m2/(i.n - 1))**0.5

