## Paper Review
Paper : 

[Applying Genetic Improvement to MiniSAT](http://www0.cs.ucl.ac.uk/staff/J.Petke/papers/Petke_2013_SSBSE.pdf)

1. *Reading* : 

Justyna Petke, William B. Langdon, Mark Harman. Applying Genetic Improvement to MiniSAT. In SSBSE 2013, Guenther Ruhe and Yuanyuan Zhang eds., Saint Petersburg, 24-26 Aug. CREST Centre, University College London, Gower Street, London.

2. *Keywords*

   1. **MiniSAT** : Is a minimalist SAT solver available [here](http://minisat.se/).
   2. **BNF (Backus Normal Form or Backus–Naur Form)** is one of the two main notation techniques for context-free grammars, often used to describe the syntax of languages used in computing.
   3. **Boolean Satisfiability Problem or SAT** : is the problem of determining if there exists an interpretation that satisfies a given Boolean formula In other words, it asks whether the variables of a given Boolean formula can be consistently replaced by the values TRUE or FALSE in such a way that the formula evaluates to TRUE. *[source](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)*
   4. **Assertion**: A statement that a predicate (Boolean-valued function, a true–false expression) is expected to always be true at that point in the code. If an assertion evaluates to false at run time, an assertion failure results, which typically causes the program to crash, or to throw an assertion exception.

3. *Notes*

   1. **Motivation** : To examine if GP is a feasible approach for generating novel optimized code by comparing the speed up of GP optimized code to human expert optimized examples.

   2. **Informative Visualization** : Very little, but a good diagram of how the GP approach was implemented. 

   ![alt text](https://github.com/meghau/fss16kms/blob/master/read/5/diagram.png)

   3. **New Results** : The paper was able to demonstrate a marginal improvement in the running time of algorithms.  Although the results were mostly obtained by removing extraneous assertions from the code, something easily achieved by a human coder, this is promising since it shows reasonable intelligence in identifying extraneous code. 

   4. **Future Work** : Finding ways to extend what can be modified so that the GP algorithm can make more significant changes. Right now it can only reorder code and remove assertions which was discovered to be limiting. 

   5. **Relation of the previous paper** : It is an extension of the program repair analysis done by --- where using some basic mutation operations, a new population was evaluated based on its performance by assigning positive weights to time improvement and bug-free behaviour.
This paper is also by the author of GISMOE challenge(base paper), which follows the basic outline laid by the authors in the original paper. 
