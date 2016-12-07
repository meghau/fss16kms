from __future__ import division, print_function

from Missions import Mission
from math import floor, e
from random import random, choice, randint
from mapGen2 import mapGen
from time import sleep
import sys
import Tkinter as tk

def dist( a, b ) : 
   return sum([ abs(x-y)**2 for x, y in zip( a, b)])**0.5

def manDist( a, b ) :
   return sum([ abs(x-y) for x, y in zip(a,b)])

mapGen[10][10] = 's'
mapGen[90][90] = 'e'
map1 = mapGen
for i,row in enumerate( map1 ) :
  for j, cell in enumerate( row ) : 
    if( cell == 's' ) : start = (i , j)
    if( cell == 'e' ) : end = (i, j) 

maxDist = dist( start, end )
minMDist = manDist( start, end )
maxMDist = len(map1) * len(map1[0])

def score( path ) :
    loc = list(start)
    for c in path :
      for _ in range(step) :
        if( c == "n" and map1[loc[0]-1][loc[1]] != 1 ) : loc[0] -= 1
        if( c == "s" and map1[loc[0]+1][loc[1]] != 1 ) : loc[0] += 1
        if( c == "e" and map1[loc[0]][loc[1]+1] != 1 ) : loc[1] += 1 
        if( c == "w" and map1[loc[0]][loc[1]-1] != 1 ) : loc[1] -= 1
    d = dist( loc, end )

    return ((d / maxDist) + ( (len(path) - minMDist) / (maxMDist - minMDist))) * 0.5

cpath  = "(0,0)(1,3)(4,5) .
"
cpath  = "eeeseeeewwww"
bpath  = cpath[:]
npath  = cpath[:]
step   = 4

cscore = score( cpath )
bscore = score( bpath )
nscore = score( npath )

print ( start, end )

scale   = 4
root    = tk.Tk()
canvas  = tk.Canvas(root,
    width=len(map1[0]) * scale,
    height=len(map1) * scale,
    borderwidth=0,
    highlightthickness=0,
    bg="black"
)
root.wm_title("minimap")
canvas.grid()
root.update()

def drawPos( pos, outline, fill ) :
  canvas.create_oval( 
    (pos[1] + .3) * scale,
    (pos[0] + .3) * scale,
    (pos[1] + .7) * scale,
    (pos[0] + .7) * scale, 
    outline=outline, fill=fill
  )

choices = ["n","s","w","e"]

ws = start[0] - end[0]
wn = end[0] - start[0]
ww = start[1] - end[1]
we = end[1] - start[1]
deno = sum([ x for x in [wn,ws,we,ww] if x > 0 ])
wn += deno
ws += deno
ww += deno
we += deno
devis = sum([wn,ws,we,ww])
wn /= devis
ws /= devis
we /= devis
ww /= devis

print( wn,ws, we,ww )
def better_choice() : 
   r = random()
   for k,v in zip([wn,ws,we,ww], ["n","s","e","w"]) : 
     if( r < k) :
       return v
     else :
       r -= k

def shake( path, p1, p2,  n ) :
  for _ in range( n ) :

    i = randint( 0, len(path) )

    if( random() < p1 ) :
      return path[:i] + path[i+1:]
    else :
      if( random() < p2 or len(path) == i ) : 
        return path[:i] + better_choice() + path[i:]
      else :
        return path[:i] + path[i] + path[i:]


fill1 = ["#0F0", "#0E0", "#0D0", "#0C0", 
         "#0B0", "#0A0", "#090", "#080", 
         "#070", "#060", "#050", "#040", 
         "#030", "#020", "#010", "#000"]
fill2 = ["#F00", "#E00", "#D00", "#C00", 
         "#B00", "#A00", "#900", "#800", 
         "#700", "#600", "#500", "#400", 
         "#300", "#200", "#100", "#000"]
fill3 = ["#00F", "#00E", "#00D", "#00C", 
         "#00B", "#00A", "#009", "#008", 
         "#007", "#006", "#005", "#004", 
         "#003", "#002", "#001", "#000"]

def drawMap( ) : 

  canvas.delete( tk.ALL )
  for i,row in enumerate( map1 ) :
    for j, cell in enumerate( row ) : 
       if( cell == 's' ) : fill = "#0F0"
       elif( cell == 'e' ) : fill ="#F00"
       elif( cell == 1 ) : fill = "#FFF"
       else: continue
       canvas.create_rectangle( j*scale, i*scale, (j+1)*scale, (i+1)*scale, fill=fill)


  for p, fillarr in zip([ cpath, bpath, npath ], [fill1, fill2, fill3]) :
      pos = list(start)
      drawPos( pos, fillarr[0], fillarr[0] ) 
      for i, c in enumerate(p) :
        for _ in range(step) : 
         fill = fillarr[ int(floor((i / len(p) * 16))) ] 
         if( c == "n" and map1[pos[0]-1][pos[1]] != 1 ) : pos[0] -= 1
         if( c == "s" and map1[pos[0]+1][pos[1]] != 1 ) : pos[0] += 1
         if( c == "e" and map1[pos[0]][pos[1]+1] != 1 ) : pos[1] += 1 
         if( c == "w" and map1[pos[0]][pos[1]-1] != 1 ) : pos[1] -= 1
         drawPos( pos, fillarr[0], fill ) 

  root.update()

def isDrunk( old, new, k, kmax ) :
  top  = old - new
  bot  = k / kmax
  p    = e**( top/(bot + 10e-7) ) 
  return p < random()

max_itr = 30000
itr = 0 
while( itr < max_itr ) : 

    itr += 1


    npath  = shake( cpath, .40, .40, int(len( map1) / 100 ) )
    nscore = score( npath )

    if( itr % 500 == 0 ):
       sys.stdout.write("\n")
       drawMap() 

    if( nscore < bscore ) :
        bpath  = npath[:]
        bscore = nscore
        sys.stdout.write("!")

    if( nscore < cscore ) :
        cpath  = npath[:]
        cscore = nscore
        sys.stdout.write("+")
    elif( isDrunk( cscore, nscore, itr, max_itr ) ) :
        cpath  = npath[:]
        cscore = nscore
        sys.stdout.write("?")
    sys.stdout.write(".")
        

    
 


