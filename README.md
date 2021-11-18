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
      1. measure the performance (time/iterations): how fast 1000 sudokus (from one folder) are solved
      2. Plots for the results
         1. matrix before and after
      3. Store the results
5. Heuristics search
      1. Start splitting from the most represented variables 
         1. in the row/col
      2. Lecture 2 part 4
      3. Search for contradictions
6. You are free to choose any programming language you fancy, but we must be able to run your SAT solver with the command SAT -Sn inputfile , for example: SAT -S2 sudoku_nr_10 , where SAT is the (compulsory) name of your program, n=1 for the basic DP and n=2 or 3 for your two other strategies, and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle). 
7. Hypotheses
      1. Do heuristics help significantly?
      Check out this report as an example:
         https://www-jstor-org.vu-nl.idm.oclc.org/stable/24505021?Search=yes&resultItemClick=true&searchText=givens+sudoku&searchUri=%2Faction%2FdoBasicSearch%3FQuery%3Dgivens%2Bsudoku%26filter%3D%26so%3Drel&ab_segments=0%2Fbasic_search_gsv2%2Fcontrol&refreqid=fastly-default%3Ab2af935edf2beea27cac151357d9612f&seq=1#metadata_info_tab_contents 
      2. What is the dependency between the sudoku size and the time?
      3. Time ~ clauses num: The dependency number of clauses (= givens? = givens at starting grid?) and time 
      4. Compare with human skills: compare the difference in computational time between 2 human approaches OR 1 human approach and the random variable selection. 
         a. Human approach 1: search for most contstraint empty cells: Start with a cell in a row/column/subgrid that has the least empty cells. 
         b. Human approach 2: Search for the minimal cell-possibilities of a value. For example: Look for only places where a 3 would fit in row 4. Use this to "guess" the cell i which the value is most likely to be (i guess this is statistics, choosing the highest possible cell) (Source: https://www.jstor.org/stable/10.2307/26061494)
      5. Update the rule base (optional)
      6. Minimal sudoku: smallest number of digits in starting ]grid that guarantees a unique solution (Gordon Royle: 17. No one yet proved 16). 
