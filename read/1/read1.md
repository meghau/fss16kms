## Mark Harman, William B. Langdon, Yue Jia, David Robert White, Andrea Arcuri, and John A. Clark. The GISMOE challenge: Constructing the pareto program surface using genetic programming to find better programs (keynote paper). In 27 th IEEE/ACM International Conference on Automated Software Engineering (ASE 2012), pages 1–14, Essen, Germany, September 2012.

## Keywords:

- ii1. Search Based Software Engineering (SBSE): SBSE is an approach to software engineering in which search-based optimizations techniques like genetic programming, simulated annealing, etc are applied to obtain near-optimal solutions to the given problem.

- ii2. Pareto Program Surface : It is the surface that is generated when programs are plotted with non-functional requirements(such as memory, execution time, power consumed, etc) as the dimensions. 

- ii3. Oracle : An oracle is a mechanism for determining whether the program has passed or failed a test. It involves comparing the output generated to the desired output for a test case.

- ii4. Sensitivity Analysis : It is a method by which we can determine which parts of the program affects the non functional requirements the most, and how. It can inform us which code to optimize.

## iii1. MOTIVATION

To reduce the burden on the software engineer by helping in the optimization of the non-functional properties and letting him focus only on the functional requirements. And to automate the process of generating multiple programs with different properties over the non-functional requirements space.

## iii2. INFORMATIVE VISUALIZATION

Visualization is done by graphing the Pareto program surface in three dimensions (x, y, z), where x is the execution time, y is the power consumed and z is the memory consumed. We can also observe *knee points*, which are regions in solution space, of rapid change in trade-offs between variables.

## iii3. RELATED WORK

The paper is based on the previous work done in using Genetic Programming for Software Engineering. Recent works including, evolving versions of  Pseudo random generator by White, and code migration of a kernel component of `gzip` UNIX utility, to GPU(an entirely different platform) by a Genetic Programming engine, has been influential.

## iii4. FUTURE WORK

It remains an interesting topic for future work to adapt techniques for syntactic and semantic similarity measure-
ment to guide such a scavenging process. There is much
work on code search and analysis [21, 73] from which we
might draw inspiration. This scavenging approach may also
raise issues concerning code provenance, which is known to
be an issue with conventionally constructed code [54].

Insight gathering: GISMOE approach can be effectively used for Analysis of code requirements. 
            
We hope that future work on the GISMOE agenda will incorporate state-of-the art test data generation techniques and advances in non-functional sensitivity analysis on which we are presently working. 

Heretical Version: Where functional requirements become one more parameters on the Paretos surface

## PROPOSED IMPROVEMENTS: 

The paper is based on a lot of study and insights gained from related work, and not on any concrete implementations, which gives rise to uncertainty. Hence, a future work with the focus of implementing and testing these ideas (which certainly would be challenging) would provide reliability.

Measurement, Visualisation, Describing Functional requirements through programming language

- iv1.

- iv2.

- iv3.

- iv4.