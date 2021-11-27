from __future__ import print_function

from pysat.formula import CNF
import math
import numpy as np
from collections import Counter

import sys
import threading


def read_DIMACS(path):
    return CNF(from_file=path).clauses


def line2DIMACS(sudoku, inverse_input_mapping):
    input_len = len(sudoku)
    table_size = int(math.pow(input_len, 0.5))
    clause_list = []
    for row in range(table_size):
        for column in range(table_size):
            current_line_index = column + table_size * row
            cell_value = sudoku[current_line_index]
            if cell_value != '.':
                clause_list.append(f"{inverse_input_mapping[row + 1]}{inverse_input_mapping[column + 1]}{cell_value} 0")
    return clause_list, table_size


def line2CNF(line, inverse_input_mapping):
    cnf_list, table_size = line2DIMACS(line, inverse_input_mapping)
    return CNF(from_string='\n'.join(cnf_list)).clauses, cnf_list, table_size


def get_digit(number, n):
    return int(number // 10 ** n % 10)


def CNFsetup2matrix(sudoku_setup_CNF, sudoku_size):
    matrix = np.zeros((sudoku_size, sudoku_size), dtype=int)
    for clause in sudoku_setup_CNF:
        for item in clause:
            matrix[get_digit(item, 2) - 1, get_digit(item, 1) - 1] = get_digit(item, 0)
    return matrix


def get_setup_info(sudoku_str, sudoku_CNF, sudoku_size):
    givens = Counter(sudoku_str.replace('\n', ''))
    givens_num = sudoku_size ** 2 - givens['.']

    col_fullness, row_fullness = get_setup_fullness(sudoku_CNF, sudoku_size)

    return givens, givens_num, row_fullness, col_fullness


def get_setup_fullness(sudoku_CNF, sudoku_size):
    matrix = CNFsetup2matrix(sudoku_CNF, sudoku_size)
    row_fullness = np.count_nonzero(matrix, axis=1)
    row_fullness = {i: v for i, v in enumerate(row_fullness, 1)}
    col_fullness = np.count_nonzero(matrix, axis=0)
    col_fullness = {i: v for i, v in enumerate(col_fullness, 1)}
    return col_fullness, row_fullness


def count_assignments(partial_assignment):
    row_assignments, col_assignments = dict((el, 0) for el in range(1, 10)), dict((el, 0) for el in range(1, 10))
    for assignment in partial_assignment:
        if assignment[1]:
            item = assignment[0]
            row_assignments[int(item[0])] += 1
            col_assignments[int(item[1])] += 1
    return row_assignments, col_assignments


def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
        print("")

try:
    import thread
except ImportError:
    import _thread as thread


def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    # print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush()  # Python 3 stderr is likely buffered.
    thread.interrupt_main()  # raises KeyboardInterrupt


def exit_after(s):
    '''
    use as decorator to exit process if
    function takes longer than s seconds
    '''

    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result

        return inner

    return outer
