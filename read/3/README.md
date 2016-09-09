## Paper Review
Paper: [A genetic programming approach to automated software repair.](https://dl.acm.org/citation.cfm?id=1570031)

1. *Reading*
    S. Forrest, W. Weimer, T. Nguyen, and C. Le Goues. A genetic programming approach to automated software repair. In Genetic and Evolutionary Computing Conference, 2009.

2. *Keywords*

    1. **Abstract Syntax Tree**: AST is a tree model of an entire program or a certain program structure. It “abstract” in the sense that some of the actual characters used in the program code do not appear in the AST.[1]

    2. **Delta debugging**: It is a methodology to automate the debugging of programs using an algorithm that builds on unit testing to isolate failure causes automatically - by systematically narrowing down failure-inducing circumstances until a minimal set remains.[2]

    3. **Fitness Function**: "A fitness function is a particular type of objective function that is used to summarise, as a single figure of merit, how close a given design solution is to achieving the set aims.” [3]. Analogously, in this paper, the solution that is being searched for is a program that achieves the required functionality while avoiding the program bugs. In the paper, the internal representation of a program is compiled into an executable one and run against the set of positive and negative test cases. Fitness is calculated as the weighted sum of the test cases passed. Uncompilable programs and those whose runtimes exceed a predetermined threshold are assigned fitness zero.

    4. **Genetic Operators**: It is an operator used in genetic algorithms to guide the algorithm towards a solution to a given problem. There are three types of genetic operators: mutation, crossover and selection. These must work in conjunction with one another in order for the algorithm to be successful. [4]

3. *Notes*

    1. **Motivation**: 

    2. **Informative Visualization**: 

    3. **Sampling Procedure**: 

    4. **Future Work**: 

4. *Proposed Improvements*
    1. The paper takes a program sample of 11
    2. The input that is given to the GP algorithm is the section with the bug and not the whole program code


5. *Connection to Previous papers*




6. *References*
[1] web.cse.ohio-state.edu/software/2231/web-sw2/extras/slides/21.Abstract-Syntax-Trees.pdf
[2] https://en.wikipedia.org/wiki/Delta_Debugging
[3] https://en.wikipedia.org/wiki/Fitness_function 
[4] https://en.wikipedia.org/wiki/Genetic_operator 





