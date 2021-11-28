import sys
import os
import time

import pandas as pd

from dpll import DPLL
from utils import read_DIMACS, save_solution2DIMACS


def run_experiment(setups_path,
                   variable_selection_method='JWTS',
                   verbose=0):
    clauses = read_DIMACS(setups_path)

    results_df = pd.DataFrame()

    # givens, givens_num, row_fullness, col_fullness = get_setup_info(sudoku, sudoku_setup_CNF, sudoku_size)
    sudoku_size = 9

    solver = DPLL(clauses,
                  variable_selection_method=variable_selection_method,
                  verbose=verbose,
                  sudoku_size=sudoku_size)

    start = time.time()
    solution = solver.backtrack(solver.clauses, partial_assignment=[], split_literal=tuple())
    solution_time = time.time() - start

    return solution

    # results_df.loc[
    #     len(results_df), ['setups_path', 'givens', 'givens_num', 'row_fullness',
    #                       'col_fullness', 'variable_selection_method', 'sat', 'solution', 'time_limit', 'time',
    #                       'backtracks']] = setups_path, givens, givens_num, row_fullness, col_fullness, variable_selection_method, *solution, time_limit, solution_time, solver.backtrack_counter
    #
    #
    # return results_df


heuristics_mapping = {'-S1': 'random', '-S2': 'fullness', '-S3': 'JWVSIDS'}

if __name__ == "__main__":
    sys.setrecursionlimit(1500)

    heuristic, filename = sys.argv[1:]
    solution = run_experiment(filename,
                              variable_selection_method=heuristic,
                              verbose=0)
    save_filename = list(os.path.splitext(filename))
    save_filename.insert(len(save_filename)-1, '_solution')
    save_solution2DIMACS(solution[1], ''.join(save_filename))