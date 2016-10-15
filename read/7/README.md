## Paper Review
Paper : 

[Using Genetic Improvement and Code Transplants to Specialise a C++ Program to a Problem Class](http://link.springer.com/chapter/10.1007%2F978-3-662-44303-3_12)  

1. *Reading* : 

J. Petke, M. Harman, W. B. Langdon, and W. Weimer. Using genetic improvement & code transplants to specialise a C++ program to a problem class. In 17th European Conference on Genetic Programming (EuroGP), Granada, Spain, April 2014.  

2. *Keywords*  

   1. **Combinatorial Interaction Testing (CIT)** : Combinatorial Interaction Testing (CIT) is a black box sampling technique derived from the statistical field of design of experiments. It has been used extensively to sample inputs to software, and more recently to test highly configurable software systems and GUI event sequences. Reference [here](http://cse.unl.edu/~citportal/).  
   2. **Code transplants** Code transplant is the process of evolving a new program by reusing and modifying existing code.  
   3. **Multi-donor transplantation** : The original program is genetically improvised using parts and structures from several “donor” programs that solve the same problem.  
   4. **Edit List**: A list of mutation changes that have to be applied to the original program to obtain the final mutated program. This method of representation saves a lot of memory as the entire mutated program need not be stored in the memory.  

3. *Notes*  

   1. **Motivation** : To investigate the application of genetic improvement (GI) to MiniSAT in order to obtain optimized code. Also introducing multi-donor software transplantation.  

   2. **Baseline Results** : The Genetically Improved MiniSAT solvers evolved in this paper are compared against four human written solvers :- MiniSAT (the original one), MiniSAT-best09 (winner of the MiniSAT-hack competition from 2009), MiniSAT-bestCIT (best performing solver from the competition when run on the CIT-specific benchmarks) and a hybrid of the above three called MiniSAT-best09+bestCIT.  

   3. **New Results** :  
        (i) The solver evolved using MiniSAT-best09 alone was not faster than the original MiniSAT solver.  
        (ii) The solver evolved using the donor MiniSAT-bestCIT was as efficient as the donor itself, but was 13% faster than the original solver.  
        (iii) Transplant from the both the above solvers resulted in a solution that was 4% faster than the original one, but had a lot of dead code, which was later removed by GP.  
        (iv) A final “combined” solver that retained only changes that did not reduce performance or correctness perfomed 17% faster than the original solver and outperformed all human-written solvers by at least 4%.  

   4. **Related Work** : Earlier, genetic programming was applied on a single program, parts of code from it were extracted, modified and reinserted back into the code, compared to the approach adopted in this paper where code is transplanted from multiple programs. Previously, Genetic improvement has been used for a variety of tasks: automation of the bug-fixing process, improvement of non-functional properties of programs, automatic migration of a system from one platform to another.  

   
4. **Relation to the previous paper** :  
    This paper tries to find a solver for the same problem as that of the previous paper, i.e. MiniSAT. The motivation behind both the papers was to obatined a genetically modified solver that outperformed the human-improved solvers.