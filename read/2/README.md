## Paper Review
Paper: [Managing performance vs. accuracy trade-offs with loop perforation.](https://dl.acm.org/citation.cfm?id=2025133)

1. *Reading*
    - S. Sidiroglou Douskos, S. Misailovic, H. Homann, and M. C. Rinard. Managing performance vs. accuracy trade-offs with loop perforation. In T. Gyiḿothy and A. Zeller, editors, 19th ACM Symposium on the Foundations of Software Engineering (FSE-19), pages 124–134, Szeged, Hungary, Sept. 2011. ACM

2. *Keywords*

    1. **Loop Perforation**: Loop Perforation involves identifying the loops in the application code that can be executed for lesser number of iterations, thereby reducing the amount of computation and increasing the performance, while obtaining sufficiently accurate results.

    2. **Criticality Testing**: It is the first phase of loop perforation, in which critical loops whose modification may lead to unexpected results are identified and filtered.  

    3. **Perforation rate**: It is a parameter for loop perforation which represents the expected percentage of loop iterations to skip. 

    4. **Pareto-optimal perforation**: A perforation which is the best in terms of both accuracy and performance.

    5. **Perforation space exploration**: It is the second phase of loop perforation, where the set of tunable loops (output of critical testing) are tested at various perforation rates and a set of Pareto-optimal loop/perforation rate pairs are returned. 

    6. **Global patterns**: In the applications that are studied in the paper, several patterns have been identified such as loops that iterate over the search space, loops that use certain search metrics to find an element, etc, which are called global patterns. Finding these patterns in an application means there is scope for loop perforation in the application.

3. *Notes*

    1. **Motivation**: Often, engineers need to strike a balance between performance and accuracy when performing computations. Maximum possible accuracy may seem desirable, but achieving that might mean sacrificing significantly on the performance. To achieve good performance while compromising on accuracy to an acceptable level, in this paper, a technique called loop perforation is explored.

    2. **Informative Visualization**: Visualization is done by plotting graphs for each perforation where the x coordinate is the percentage of accuracy loss and the y coordinate is the mean speedup of the perforation. The graph is called performance vs accuracy trade-off space.

    3. **Related Work**: In the past, there have been several efforts to trade accuracy with different factors like performance, robustness, energy consumption, etc. Among these efforts, one of them explored task skipping (which is comparable to loop perforation) to reduce resource usage when maintaining acceptable accuracy. In another effort, programmers had to provide several implementations for a specific functionality and the implementations represented different points on the performance-accuracy space. An appropriate implementation would be chosen according to the problem at hand. Yet another work called Autotuners involved exploration of alternatives that had the exact same accuracy.

    4. **New Results**: The results presented in this paper are better  compared to older ones due to the following reasons:
        1. Developers do not have to provide multiple implementations for the same functionality. The trade-off space is automatically explored to find alternatives.  
        2. There are several global computational patterns defined in the paper which can be used to identify parts of an applications where loop perforation can be applied.  
        3. Loop perforation, unlike autotuners (mentioned in RELATED WORK), does not explore alternatives with exact same accuracy, but with accuracy within a particular bound.  

4. *Proposed Improvements*

    - 1. 
    - 2.
    - 3.
    - 4.

