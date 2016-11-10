from Table import Table, Reader 
from Stats import *

t = Reader( "./output.csv" ).table()

print( repr(t) ) 
 
col1 = ["steps"]
col2 = ["health"]
col3 = ["gold"]
col4 = ["time"]
col5 = ["win"]

for col in 
for row in t : 
   col1.append( row[0] )
   col2.append( row[1] )
   col3.append( row[2] )
   col4.append( row[3] )
   col5.append( row[4] )

rdivDemo( [
   col1, 
   col2, 
   col3, 
   col4, 
   col5 
])
