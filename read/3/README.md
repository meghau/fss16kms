## Paper Review
Paper: [A genetic programming approach to automated software repair.](https://dl.acm.org/citation.cfm?id=1570031)

1. *Reading*
    S. Forrest, W. Weimer, T. Nguyen, and C. Le Goues. A genetic programming approach to automated software repair. In Genetic and Evolutionary Computing Conference, 2009.

2. *Keywords*

    1. **Abstract Syntax Tree**: AST is a tree model of an entire program or a certain program structure. It “abstract” in the sense that some of the actual characters used in the program code do not appear in the AST.[1]

    2. **Delta debugging**: It is a methodology to automate the debugging of programs using an algorithm that builds on unit testing to isolate failure causes automatically - by systematically narrowing down failure-inducing circumstances until a minimal set remains.[2]

    3. **Fitness Function**: “A fitness function is a particular type of objective function that is used to summarise, as a single figure of merit, how close a given design solution is to achieving the set aims.” [3]
    Analogously, in this paper, the solution that is being searched for is a program that achieves the required functionality while avoiding the program bugs. In the paper, the internal representation of a program is compiled into an executable one and run against the set of positive and negative test cases. Fitness is calculated as the weighted sum of the test cases passed. Uncompilable programs and those whose runtimes exceed a predetermined threshold are assigned fitness zero.

    4. **Genetic Operators**: It is an operator used in genetic algorithms to guide the algorithm towards a solution to a given problem. There are three types of genetic operators: mutation, crossover and selection. These must work in conjunction with one another in order for the algorithm to be successful. [4]

3. *Notes*

    1. **Motivation**: Genetic Programming (GP) has not replaced human programmers, who still develop, maintain, and repair computer programs largely by hand. In this paper, we describe how GP can be combined with program analysis methods to repair bugs in off-the-shelf legacy C programs.

    2. **Informative Visualization**: Visualization is done by plotting two kinds of graphs: first with generations on the x-axis and average fitness on the y-axis. These graphs depict how the average fitness changes over time in one GP trial. The second type has natural logarithm of weighted path length on the x-axis and the natural logarithm of the total number of fitness evaluations performed before the primary repair is found on the y-axis. This graph shows that GP search time scales with execution path size

    3. **Related Work**: Previously Finite State Machines were used to write formal specifications that a modified program had to follow, which is not the case in the approach described in the paper. The approach deals with long term program repair, but further research in short term repair strategies like patching buggy data structures can complement this paper’s work. 

    4. **Future Work**: Suggestions for future work include: variation of repairs after minimization, comparison of repair quality to human-engineered solutions, necessity of crossover to the GP search, optimality of GP design, possible improvement of results by using a multi-objective fitness function, exploration of different parameter values, selection strategies, and operator design. In addition, there are also suggestion to explore differential weighting on the test cases and dynamic selection of test cases to be tested with the fitness function.

4. *Proposed Improvements*
    1. The paper takes a limited program sample of 11 with varying lines of code. There is no generalizing behaviour that could be extracted about a program of a particular size.  
    2. The cost of repairing or the algorithmic complexity related with Genetic Operations such as inserting, deleting, modifying, statements and subsequent crossover, mutation and their relation with lines of code could have been revealed.
    3. Visualization of Abstract Syntax Tree space, would have helped in understanding the genetic operators decisions.
    4. Mutation operator, and statement to insert are chosen at random. It would be interesting to see how a more predictive approach compares.

    
5. *Connection to Previous papers*

[GISMOE Challenge paper](https://github.com/meghau/fss16kms/blob/master/read/2/README.md) cites automated program repair papers for using Genetic Programming  in non-trivial Bug fixing. This paper lays the groundwork for many things GISMOE challenge talks about.

6. *References*
- [1] http://web.cse.ohio-state.edu/software/2231/web-sw2/extras/slides/21.Abstract-Syntax-Trees.pdf
- [2] https://en.wikipedia.org/wiki/Delta_Debugging
- [3] https://en.wikipedia.org/wiki/Fitness_function
- [4] https://en.wikipedia.org/wiki/Genetic_operator







