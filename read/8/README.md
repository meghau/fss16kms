## Paper Review
Paper : [Automated software transplantation 2015](https://dl.acm.org/citation.cfm?id=2771796&CFID=682409981&CFTOKEN=89856133)

1. *Reading* : 

Earl T. Barr , Mark Harman , Yue Jia , Alexandru Marginean , Justyna Petke, Automated software transplantation, Proceedings of the 2015 International Symposium on Software Testing and Analysis, July 13-17, 2015, Baltimore, MD, USA 

2. *Keywords*  

   1. **Automatic Transplantation** : An application of Genetic Improvement to identify and port(extract-isolate-embed) features from a host application to a donor application.
   2. **in-situ Testing** : A form of testing that con-
   strains the input space of traditional testing to more closely
   approximate behaviourally relevant inputs.
   3. **Regression Testing** :  Testing carried out to ensure that changes made in the fixes or any enhancement changes are not impacting the previously working functionality. It is executed after enhancement or defect fixes in the software or its environment.

3. *Notes*  

   1. **New Results** :  
        (i) A wide variety of real world applications were successfully tested and used as donors and hosts for feature transplantation. The results were generalized as every donor was paired with every host, and even itself for sanity check.
        (ii) uTrans(algorithm) and uSCALPEL(framework) were demonstrated to be effective. Given the entry point, the approach can identify all code associated with a feature, and extract it. It can also automatically map donor variables to host variables.
        (iii) Through the 2 testing framweorks - regression testing, to test if the host hasn't broken after transplantion and in-situ testing, to test the effectiveness of new added organs(features), results were successfully established.
        (iv) Automated Transplantation was shown to reduce the time and programmer workload on a big feature of real work application(VLC media player).


   2. **Case Study** : The authors after porting small features to applications, tested the framework by porting a H264 encoder from x264(host) to VLC(donor). The organ in this case was very large (263k LoC) and multi threaded in nature. The crossover rate was kept 0.5, with fixed 2 point or uniform crossover implementation. Selection policy was top 10% of children were selected with rest decided by tournament selection of 60% population. 

   3. **Baseline Results** : The baseline results were time taken in porting tasks done by programmers. In the case study, it was estimated that over 11 years and 39 updates, it took an average of 20 days(of elapsed time) for VLC developers to port x264 encoder. The framework completed the same task in 26 hours(continuous time).

   4. **Visualizations** : The authors provide architectural diagrams for the proposed algorithm and approach. A graph flow for identifying organ; Mutation, Crossover, Validation and methods were visualized. The resulting code after transplantation was visualized by diff command, and highlighting modified sections.
   
4. *Proposed Improvements* :
    - One assumption in the paper was that organs need very few of statements in their donor. The initial population was generated with one line of source code and then mutated. This can be one a limiting factor for identifying and porting complex functions.
    - The framework can handle only C programs, uses static analysis, and would be difficult to port for dynamic languages.
