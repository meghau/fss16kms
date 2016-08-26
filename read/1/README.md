## Mark Harman, William B. Langdon, Yue Jia, David Robert White, Andrea Arcuri, and John A. Clark. The GISMOE challenge: Constructing the pareto program surface using genetic programming to find better programs (keynote paper). In 27 th IEEE/ACM International Conference on Automated Software Engineering (ASE 2012), pages 1–14, Essen, Germany, September 2012.

## Keywords:

- ii1. Search Based Software Engineering (SBSE): SBSE is an approach to software engineering in which search-based optimizations techniques like genetic programming, simulated annealing, etc are applied to obtain near-optimal solutions to the given problem.

- ii2. Pareto Program Surface : It is the surface that is generated when programs are plotted with non-functional requirements(such as memory, execution time, power consumed, etc) as the dimensions. 

- ii3. Oracle : An oracle is a mechanism for determining whether the program has passed or failed a test. It involves comparing the output generated to the desired output for a test case.

- ii4. Sensitivity Analysis : It is a method by which we can determine which parts of the program affects the non functional requirements the most, and how. It can inform us which code to optimize.

## iii1. MOTIVATION

The authors put forward a vision to automate much of the slow and inefficient way we currently develop software, thus reducing the burden on humans, who can then focus better on the earlier stages of the development process. Recent advancements in Genetic Programming have shown that we can efficiently and quickly generate very large space of candidate solutions which can then be navigated for optimality, by humans.

## iii2. INFORMATIVE VISUALIZATION

Visualization is done by graphing the Pareto program surface in three dimensions (x, y, z), where x is the execution time, y is the power consumed and z is the memory consumed. We can also observe *knee points*, which are regions in solution space, of rapid change in trade-offs between variables. 

## iii3. RELATED WORK

The paper proposes an approach based on Search based optimisation techniques and leverages previous work done in fields such as Genetic Programming and Evolutionary approaches to Software Engineering problems. Recent works include evolving versions of Pseudo random generator by White, and code migration of a kernel component of `gzip` UNIX utility, to GPU(an entirely different platform) by a GP(Genetic Programming) engine. In software companies like Google, Microsoft etc, GP engines have recently been used for Bug detection and fixing These works lay the foundation for GISMOE approach. GP

## iii4. FUTURE WORK

The paper provides a vision for automation techniques, for which research data from many sub-fields will be required. One such field is how functional requirements can be treated in the system as just another dimension in the non-functional requirement space, but with a higher priority. This can give us approximate solutions which can be many times as efficient as fully-correct solutions. Also, GISMOE relies heavily on the quality test data generation and testing methodologies, which would require future work.  

## PROPOSED IMPROVEMENTS: 

- iv1. The paper is based on a lot of study and insights gained from related work, and not on any concrete implementations, which gives rise to uncertainty. Hence, a future work with the focus of implementing and testing these ideas (which certainly would be challenging) would provide reliability.

- iv2. In addition to Search Based Optimization techniques, the paper could also incorporate or imagine a place for Machine Learning techniques like Deep Learning, which have seen recent advancements.

- iv3. The authors propose specifying functional requirements, but how that is do be done is not made entirely clear.  

- iv4. The authors could talk more about interpreting the multi-objective space in terms of tradeoffs, priority of objectives; zooming in a particular region in space.