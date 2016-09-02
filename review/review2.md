# Review-2

### Lecture Date : 08/30/16

##  Practice

#### 1. Iterators

1a. The following code has a bug. The countdown stops at 10 (no 9,8,7...). Why?

```python
def countdown(n):
   while n >= 0:
     return  n
     n -= 1

print("We are go for launch")
for x in countdown(10):
   print(x)
print("lift off!")
```
Ans. Because the function doesn't remember the value of x, and in each iteration of for gets "10" as the argument. To fix it we should replace the `return` with `yield`


1b. Modify the following code such that the final `out` list
only contains numbers over 20

```python
def items(x, depth=-1):
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y, depth+1):
        yield z
  else:
    yield x

out = []
for x in items(  [10,[ 20,30],
                        40,
                        [   (  50,60,70),
                            [  80,90,100],110]]):
   out += [x]
print out
``` 

Ans.
```python
def items(x, depth=-1):
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in items(y, depth+1):
        yield z
  else:
    yield x

out = []
for x in items(  [10,[ 20,30],
                        40,
                        [   (  50,60,70),
                            [  80,90,100],110]]):
   if x>20:
    out += [x]
print out
```


1c. Repeat the above, this time using _list comprehensions_.

Ans.
```python
out = [x for x in items(  [10,[ 20,30],
                40,
                [   (  50,60,70),
                    [  80,90,100],110]]) if x > 20]

print out
```


1d. Using list comprehensions, write a function that returns only non-whitespace
in a string. Hint:

```python
import string
string.whitespace # <== contains all whitespace chars
```

Ans.
```python
def remove_whitespace(a_string):
    import string
    return "".join([s for s in a_string if s not in string.whitespace])

print(remove_whitespace("hey how    are you    !"))
```


1e. Using list comprehensions and the following code,
return all lines in a multi-line
strings that  are (a) non-blanks and (b) longer than 20
characters in length. Hints: `not str` returns `True` for non empty strings.

```python
def lines(string):
  tmp=''
  for ch in string: 
    if ch == "\n":
      yield tmp
      tmp = ''
    else:
      tmp += ch 
  if tmp:
  yield tmp
```

Ans.
```python
def remove_whitespace(a_string):
    import string
    return "".join([s for s in a_string if s not in string.whitespace])

def atleaset_20(string):
    return [line for line in lines(string) if remove_whitespace(line) and len(line)>20]
```

1f. Whats the logical error in the code? I need a list of 20 random numbers
```python
import random
x = []
for _ in range(20):
  random.seed(1)
  x.append(random.random())
print(x)
```
  Correct it by moving 1 line.

Ans.
```python
import random
x = []
random.seed(1)
for _ in range(20):
    x.append(random.random())
print(x)
```
  
1g. Write a small snippet for a random odd integer generator between 1 and 1000. (Hint: yield)

Ans.
```python
from __future__ import division

def random_odd(start=1,stop=1000,count=10):
    import random
    for i in range(count):  
        start = start+1 if start%2==0 else start
        step = 2
        end = int((stop-start)/step)
        x = random.randint(0,end)
        y = x*step+start
        yield y

print(list(random_odd(1,1000,20)))
```
  
#### 2. Dunders


2a. What are the dunders in the following code? For each one,
use them in a code snippet.

```
class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)
```

2b. In the above, what is the magic __dict__ variable?

2c. What would happen if the _last line_ in the following `__iadd__` method
was deleted?

```python
r = random.random
rseed = random.seed

class Some:
  def __init__(i, max=8): 
    i.n, i.any, i.max = 0,[],max
  def __iadd__(i,x):
    i.n += 1
    now = len(i.any)
    if now < i.max:    
      i.any += [x]
    elif r() <= now/i.n:
      i.any[ int(r() * now) ]= x 
    return i
```	


2d. In English, explain what the above `Some` class  does. Use it in a loop
to keep `Some` numbers in the series 0,1,2,...999.

#### 3. 8 Queens
You've seen the knightstour. Can you code up the 8 queens problem in python? (https://en.wikipedia.org/wiki/Eight_queens_puzzle)

#### 4. FSM
What is a finite state machine?
Can you describe an fsm in python for the following problem.
You're in a bar.
 1. You start of sober.
 2. If you are sober you take a drink
 3. If you are drunk and take a drink then there is a 80% chance you get drunk and there is a 20% chance you pass out.
 4. If you are drunk and do not take a drink, there is a 50% chance you get sober.
 5. If you pass out you obviously stop drinking

