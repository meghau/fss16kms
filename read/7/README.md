## Paper Review
Paper : [Reducing Energy Consumption Using Genetic Improvement 2015](https://dl.acm.org/citation.cfm?id=2754752&CFID=681984198&CFTOKEN=78435507)

1. *Reading* : 

Bobby R. Bruce , Justyna Petke , Mark Harman, Reducing Energy Consumption Using Genetic Improvement, Proceedings of the 2015 on Genetic and Evolutionary Computation Conference, July 11-15, 2015, Madrid, Spain

2. *Keywords*  

   1. **Genetic Improvement** : An area of Search Based Software Engineering which seeks to improve software’s non-functional properties by treating program code as if it were genetic material which is then evolved to produce more optimal solutions.
   2. **Downstream applications** : The applications that use the upstream(orignal) MiniSAT solver as the basis to do more complex tasks.
   3. **Ensemble Computation** : The study of an NP-complete variant of the Boolean circuit problem where one must find the smallest circuit that satisfies a set of Boolean functions simultaneously. This problem can be translated into a satisfiability problem.
   4. **AProVE**: Automated Program Verification Environment is a system for the generation of automated termination proofs of term rewrite systems. AProVE uses a Boolean satisfiability solver to determine which paths can or cannot be reached.

3. *Notes*  

   1. **Motivation** : The authors state a two fold need to worry about energy consumption of an application. 
        - The increase of smartphone and cloud server usage, which benefit greatly from energy efficiency. Our energy grid is affected by servers and optimizing them can help in reduction of CO2 emission. 
        - Other is the programmer disconnect between source code written and energy consumption of the compiled application.

   2. **Baseline Results** : The downstream applications, which use MiniSAT solver tested here are CIT, Ensemble and AProVE. The modified and the unmodified versions are run 20 times and averaged for execution time. The fitness(and the correctness) of the solutions is also tested against the original versions and only those are measured which are correct.

   3. **New Results** :  
        (i) Genetic Improvement technique was demonstrated to directly work with source code.
        (ii) The investigation discovered that GI optimizes those areas or cases of source code which run very rarely, but incur significant cost. An example was a random number generator which ran 2% of the time. Another was an assert statement which was violated very rarely.
        (iii) Optimizing on a small area of code which led to the best solutions not having more than one modification
        (iv) An optimized MiniSAT solver of a downstream application in some cases can be generalized for all problems, for improvements.

   4. **Related Work** : Genetic Improvement has been demonstrated to effectively reduce execution time while working with compiled code in the post compilation process. Also it has been tested on the specific SAT solver problem to improve it by 17%. 

   
4. *Relation to the previous paper* :  
    The investigation uses MiniSAT solver as a base problem to optimize, through genetic improvements. The authors of this paper have tried optimizing MiniSAT problem before with different metrics and behaviour. 

5. *Proposed Improvements* :
    - The investigation was platform specific in nature. The applications tested were CPU-bound, single threaded. The architecture was Intel Core processors, and the Operating system was MacOSX. A more generalized testing framework would have been an improvement.
    - The limited number of downstream applications tested (3) limits the generalization of the results on all MiniSAT solvers.
    - The mutation, selection and crossover policy of top 5 best solutions going unmodified, and rest having 50% probility of mutation might have been inadequate to produce more effective mutations.
    - The mutation were only allowed from inside the program source code(which were typically 500 lines) based on the assumption that source code is generally redundant. This assumption might not be true when source code is very small. 
    - The optimizations could be seen as general programming bugs, having no strong co-relation to energy consumption.
