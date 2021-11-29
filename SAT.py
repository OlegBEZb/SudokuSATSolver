import sys
import os
import time

from dpll import DPLL
from utils import read_DIMACS, save_solution2DIMACS


def run_experiment(setups_path,
                   variable_selection_method='JWTS',
                   verbose=0):
    clauses = read_DIMACS(setups_path)

    sudoku_size = 9

    solver = DPLL(clauses,
                  variable_selection_method=variable_selection_method,
                  verbose=verbose,
                  sudoku_size=sudoku_size)

    print(f"Having {len(solver.clauses)} clauses")

    start = time.time()
    solution = solver.backtrack(solver.clauses, partial_assignment=[], split_literal=tuple())
    solution_time = time.time() - start
    print(f"Solved in {solution_time} sec")

    return solution


heuristics_mapping = {'-S1': 'random', '-S2': 'fullness', '-S3': 'JWVSIDS'}

if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    heuristic, filename = sys.argv[1:]
    solution = run_experiment(filename,
                              variable_selection_method=heuristics_mapping[heuristic],
                              verbose=0)
    save_filename = list(os.path.splitext(filename))
    save_filename.insert(len(save_filename) - 1, '_solution')
    save_solution2DIMACS(solution[1], ''.join(save_filename))
