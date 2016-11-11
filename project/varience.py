from __future__ import division
from Util import TwoWayDict
from makemap import colorMap, getMap, colorStr
from gen_randmap import genMap
import sys 
from time import sleep
import Tkinter as tk
import random 

mymap = genMap

for i, row in enumerate(mymap) :
   for j, cell in enumerate(row) : 
      if cell == 6 : start = (i,j)
      if cell == 3 : end = (i,j)

"""
init TKINTER 
"""
scale   = 4
root    = tk.Tk()
canvas  = tk.Canvas(root,
    width=len(mymap[0]) * scale,
    height=len(mymap) * scale,
    borderwidth=0,
    highlightthickness=0,
    bg="black"
)

root.wm_title("minimap")
canvas.grid()
root.update()

prob = [0.35,0.50,0.65,1.00]

  
def shake() :

   a = [ random.random() for _ in range(4) ]
   a[0] = a[0] * (1 + ( random.random() / 3 ) ) 
   a[3] = a[3] * (1 + ( random.random() / 3 ) ) 
   b = sum( a )
   c = [ x / b for x in a ]
   d = [sum(c[0:x+1]) for x in range(4)  ]
   prob = d

   sys.stderr.write( "Updated probs : " + str( prob ) ) 

def step( pos ) :
    r = random.random()
    if( r < prob[0] ) :
        return ( pos[0] + 1, pos[1] ) 
    if( r < prob[1] ) :
        return ( pos[0] - 1, pos[1] ) 
    if( r < prob[2] ) :
        return ( pos[0], pos[1] - 1) 
    else : 
        return ( pos[0], pos[1] + 1) 

def drawMap( ) : 

  canvas.delete( tk.ALL )
  for i,row in enumerate( mymap ) :
    for j, cell in enumerate( row ) : 
       canvas.create_rectangle( j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=colorStr[cell])
  root.update()

def drawPos( pos, color ) :
  (i,j) = pos
  canvas.create_rectangle( j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=color)
  root.update()

print( "steps, health, gold, time, win" ) 

for i in range( 10000 ) :

   if ( i % 100  == 0 ) : 
      shake()

   drawMap()    
   pos = start


   steps  = 0 
   health = 1000
   gold   = 0
   time   = 0
   win    = 0 


   while( True ) : 
      drawPos( pos , colorStr[6] ) 
      pos2 = step( pos ) 
      cell = mymap[pos2[0]][pos2[1]] 

      time += 1
      if( cell != 0 and cell != 1): 
         pos = pos2
         steps += 1

      if( cell == 1 ):
        if( gold > 50 ) :
           gold -= 50
           pos = pos2
           steps += 1

      if( cell == 3 ):
         gold += 100
         win   = 1
         break

      if( cell == 5 ) : 
         gold += 10

      if( cell == 4) :
         health -=100 

      if( cell == 7 ) : 
         time += 1
         steps += 1

      if( cell == 8 ) : 
         health += 50

      health -= 1
      steps  += 1

      if( health < 0 ) :
         break 
   print( "%d, %d, %d, %d, %d" %(steps, health, gold, time, win))

