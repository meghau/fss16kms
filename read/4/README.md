## Paper Review
Paper: [Multi-objective improvement of software using co-evolution and smart seeding.](http://link.springer.com/chapter/10.1007/978-3-540-89694-4_7)

1. *Reading*
    A. Arcuri, D. R. White, J. A. Clark, and X. Yao. Multi-objective improvement of software using co-evolution and smart seeding. In 7th International Conference on Simulated Evolution and Learning (SEAL 2008), pages 61–70, Melbourne, Australia, December 2008. Springer. 

2. *Keywords*

    1. **Multi-objective optimization (MOO)**: Multiobjective optimization involves minimizing or maximizing multiple objective functions subject to a set of constraints. [1]
    
    2. **Strength Pareto Evolutionary Algorithm (SPEA)**: Strength Pareto Evolutionary Algorithm is a Multiple Objective Optimization algorithm and an Evolutionary Algorithm. The objective of the algorithm is to locate and and maintain a front of non-dominated solutions, ideally a set of Pareto optimal solutions. The algorithm can be found in [3]. 
    
    3. **Branch coverage**: “Branch coverage is a testing method, which aims to ensure that each one of the possible branch from each decision point is executed at least once and thereby ensuring that all reachable code is executed. That is, every branch taken each way, true and false.” [2] In the paper, branch coverage is used to generate a set of test cases with high behavioral diversity.
    
    4. **Semantic Score**: In this paper, semantic score is a component of the fitness function of a GP individual. It is defined as the sum of the errors from the expected outcomes.
    
3. *Notes*

    1. **Motivation**: Several factors have to be considered when optimizing a software for the non-functional properties such as dependence on low-level details that are invisible to a developer or external factors like operating system and memory cache events. This makes manual optimization impossible. Hence, Genetic programming's success in optimization problems is exploited for the task. In this paper, only execution time is optimized, but a similar technique could be used to optimize other properties as well. 
    
    2. **Informative Visualization**: Visualization is done by plotting graphs for each GP individual (program) where non-functional properties are along the x-axis and number of errors are along the y-axis.
    
    3. **New Results**: Some important results obtained in this paper:  
        - In general GP, initial population is sampled at random. In the paper, initial population seeded based on the original program has proved to produce better results.  
        - Performance can be improved by using the application of co-evolution.  
        - The experiments in the paper indicate small populations over a large number of generations are better whereas usually in general GP, a large population with small number of generations is better.  
    
    4. **Future Work**: Future work would include testing the results obtained in this paper for other problems, investigating optimal parameter settings, exploring alternative seeding strategies and using extended evolutionary runs.

4. *Scope for Improvement*  
    In the paper, the process of selection of parameters for model construction hasn't been explained in sufficient detail. In addition, the model-based approach for evaluating the non-functional criteria doesn't seem reliable.  

5. *Connections to previous papers*  
    The motivation is similar to that of the orginal [GISMOE Challenge paper](https://github.com/meghau/fss16kms/blob/master/read/1/README.md), i.e. to optimize the non-functional properties of software.

6. *References*
    - [1] http://www.mathworks.com/discovery/multiobjective-optimization.html
    - [2] http://www.tutorialspoint.com/software_testing_dictionary/branch_testing.htm
    - [3] http://www.cleveralgorithms.com/nature-inspired/evolution/spea.html

