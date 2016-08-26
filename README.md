# CS591 Automated Software Engineering 2016

### Team:   
1. Siddharth Sharma  
2. Megha Umesha


## Review 0
1. *Differentiate between Data Mining and Model Based Optimization.*
    
    According to my understanding in class, Data mining has discrete data points, leading to gaps in the training data, whereas in model-based optimization, the data points can be interpolated and we can resample any number of points between any two given points and try to obtain the optimum value.  
    Note: In my opinion, data mining is a very broad term and there do exist several methods in data mining that interpolate the data points like linear regression, and hence such generalization may seem incorrect.  
  
2. *How is Model-based Automated Software Engineering(MASE) different from traditional SE?*  

    Traditional SE focuses on services that fulfill requirements, while MASE focuses on searching interesting patterns in the software that solve a particular requirement, which would help in model evolution. In MASE, we also explore existing models.  
  
3. *Give an example of multi objective optimization.*

    A typical example would be of a student trying to make the most of the time available to him. Suppose the student has taken ’n’ number of courses and has to perform decently in every course, then he will have to strike a balance, managing and allocating sufficient time to work on for each course, so that he doesn’t spend too much only on one subject and does well in that particular one whereas fails in another. The objective here would be to well in subjects 1 to n.

## Review-1

## Theory
______
1. *What does a python function return by default?*
    
    `None` object.

1. *How do you access global variables in python?*
    
    Declaring them inside function with `global` keyword.

1. *What is a decorator?*
    
    Decorator is a feature in Python to modify behaviour of a function. At compile time, the Decorator is passed the function on which it is applied to, and returns the modified function.   

1.  *What does a seed do in a random number generator?*
    
    A random number generator works by taking a number at the start, and performing *psuedorandom* operations on it to compute the next number, and so on. The seed is that first number.

1. *What happens if an assertion is false?*
    
    An `AssertionError` exception is thrown.

2. *Give a use case for `__lt__`*
    
    To compare strings based on the sum of ascii values of each character we can overwrite default `__lt__` behaviour. ex - `'bz'>'za'` which will evaluate to `True`.

3.  *What does `__str__` do?*
    
    When you print an object or call str(object), `__str__` method of the class is called, to convert it into a string value.
 
##Practice
______
1. For each of the following, can you offer a 3 line code snippet to demo the idea?
  * Classes
       ```
        class MyFraction():
            def __init__(self,num,denom):
                self.denom = denom
                self.num = num
                print("Object created")

        m = MyFraction(4,5)
       ```
  * Functions
        ```
        def add(x,y):
            return x+y

        print(add(8.5,9))
        ```
  * default params
        ```
        def print_greeting(s='Hello'):
            print(s)

        print_greeting()
        print_greeting('Bye!')
        ```
  * variable lists args
        ```
        def add_all(*args):
            return sum(args)

        print(add_all(1,2,3,4,5))
        ```
  * variable dictionary args
        ```
        def dict_args(**kwargs):
            return kwargs.keys(),kwargs.values()
        
        print(dict_args(a="hello",b="world"))
        ```
  * decorators
        ```
        def decorator(funct):
            def new_funct():
                print("starting ..")
                funct()
                print("stopping ..")
            return new_funct()

        @decorator
        def hello():
            print("Hello")

        ```
  * exception handling
        ```
        try:
            s = 4/0
        except:
            print("Error")
        finally:
            print("Back to normality")
        ```
  
2. Write a function that takes 2 args(Arg1 and Arg2) such that Arg 1 is a list of numbers, Arg2 is a number. Return a list of size Arg2 from Arg1 such that no duplicates are present. eg
```
def func(arg1, arg2):
  do something
  
x = func([1,2,3,4,5,6,7,8], 4)
# x is [6,2,7,1]
```

Solution:
```
def func(lst,length):
    return list(set(lst))[:length]
```
3. Give a snippet highlighting inheritance in python
```
class Parent():
    def __init__(self,name):
        print("Parent object created")
        self.name = name
    def get_name(self):
        return self.name

class Child(Parent):
    def __init__(self,name,age):
        Parent.__init__(self,name)
        print("Child object created")
        self.age = age
    def get_age(self):
        return self.age

p=Parent("George")
print(p.get_name())
c = Child("Fred",15)
print(c.get_name(),c.get_age())
```
