## Paper Review
Paper: [A genetic programming approach to automated software repair.](https://dl.acm.org/citation.cfm?id=1570031)

1. *Reading*
    S. Forrest, W. Weimer, T. Nguyen, and C. Le Goues. A genetic programming approach to automated software repair. In Genetic and Evolutionary Computing Conference, 2009.

2. *Keywords*

    1. **Abstract Syntax Tree**: AST is a tree model of an entire program or a certain program structure. It “abstract” in the sense that some of the actual characters used in the program code do not appear in the AST.[1]

    2. **Delta debugging**: It is a methodology to automate the debugging of programs using an algorithm that builds on unit testing to isolate failure causes automatically - by systematically narrowing down failure-inducing circumstances until a minimal set remains.[2]

    3. **Fitness Function**: “A fitness function is a particular type of objective function that is used to summarise, as a single figure of merit, how close a given design solution is to achieving the set aims.” [3]
Analogously, in this paper, the solution that is being searched for is a program that achieves the required functionality while avoiding the program bugs. In the paper, the internal representation of a program is compiled into an executable one and run against the set of positive and negative test cases. Fitness is calculated as the weighted sum of the test cases passed. Uncompilable programs and those whose runtimes exceed a predetermined threshold are assigned fitness zero.

    4. **Genetic Operators**: 

3. *Notes*

    1. **Motivation**: 

    2. **Informative Visualization**: 

    3. **Sampling Procedure**: In the past, there have been several efforts to trade accuracy with different factors like performance, robustness, energy consumption, etc. Among these efforts, one of them explored task skipping (which is comparable to loop perforation) to reduce resource usage when maintaining acceptable accuracy. In another effort, programmers had to provide several implementations for a specific functionality and the implementations represented different points on the performance-accuracy space. An appropriate implementation would be chosen according to the problem at hand. Yet another work called Autotuners involved exploration of alternatives that had the exact same accuracy.

    4. **Future Work**: 

4. *Proposed Improvements*

    
5. Connection to Previous papers

6. References
[1] web.cse.ohio-state.edu/software/2231/web-sw2/extras/slides/21.Abstract-Syntax-Trees.pdf
[2] https://en.wikipedia.org/wiki/Delta_Debugging
[3] https://en.wikipedia.org/wiki/Fitness_function 





