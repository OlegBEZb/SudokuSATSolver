# SudokuSATSolver
Selected internal format:
`[[('FFF', False), ('11B', False)], # one clause
[(999, True), (123, False)] # second 
]`
1. ~~Combine base rules with the case-specific~~
2. ~~Write simple tests for SAT solver (may be a nice contribution to the grade)~~
3. General SAT solver (clauses as input)
   1. ~~Sequentially go through the tree and return the decision + the solution if applicable~~
   2. Store output
4. Experimentation
      1. time limitation for the case (1min)
      2. measure the performance (time/iterations/backtracks): how fast 1000 sudokus (from one folder) are solved
      3. Plots for the results
         1. matrix before and after
      4. Store the results / launch from command
      5. check all methods on a fixed set of tasks
      6. check compatible methods on hard cases for one
5. Heuristics search
      1. Start splitting from the most represented variables 
         1. in the row/col
      2. Lecture 2 part 4
      3. Search for contradictions
      4. Check literature
      5. Launch without a setup
      6. How many givens we need. What is the dependency
         1. For each case we note the size of givens
         2. Separate exp when having a solved case, we try to solve it without one value, without two ...
6. You are free to choose any programming language you fancy, but we must be able to run your SAT solver with the command SAT -Sn inputfile , for example: SAT -S2 sudoku_nr_10 , where SAT is the (compulsory) name of your program, n=1 for the basic DP and n=2 or 3 for your two other strategies, and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle). 
7. Hypotheses
      1. Do heuristics help significantly?
      2. What is the dependency between the sudoku size and the time
      3. Time ~ clauses num
      4. Compare with human skills (have to have some API or specific data)
      5. Update the rule base (optional)
      6. 