import random
from copy import deepcopy
from itertools import chain
from typing import List, Tuple
from itertools import chain
from utils import count_assignments, get_setup_fullness
import functools
import operator
import collections

class DPLL:
    def __init__(self, clauses, variable_selection_method='random', verbose=0,
                 sudoku_size=9, row_fullness=None, col_fullness=None):

        self.clauses = clauses
        # extracts unique variable from DIMACS format
        self.variables_set = set(map(str, (map(abs, chain.from_iterable(self.clauses)))))
        # converts into internal format where each literal looks like (var_name, True)
        self.clauses = [[(str(abs(literal)), literal > 0) for literal in c] for c in self.clauses]

        self.variable_selection_method = variable_selection_method
        self.backtrack_counter = 0

        self.sudoku_size = sudoku_size
        self.row_fullness = row_fullness
        self.col_fullness = col_fullness

        self.verbose = verbose

    @staticmethod
    def neg(literal):
        return (literal[0], not literal[1])

    def select_random_variable(self, partial_assignment: List[Tuple]):
        if self.verbose:
            print('random variable selection')
        if self.verbose > 4:
            print('inside variable selection partial_assignment', partial_assignment)
        already_split = set([literal[0] for literal in partial_assignment])
        if self.verbose > 4:
            print('already_split', already_split)
        return random.choice(list(self.variables_set - already_split))

    def get_literal_occurances(self, clauses: List[Tuple], partial_assignment: List[Tuple]):
        if self.verbose:
            print('Jeroslow-Wang variable selection')
            print('inside variable selection partial assignment', partial_assignment)
        already_split = set([literal[0] for literal in partial_assignment])
        counter = {}
        for clause in clauses:
            for literal in clause:
                if literal[0] not in already_split:  # check variable
                    if literal in counter:
                        counter[literal] += 2 ** -len(clause)
                    else:
                        counter[literal] = 2 ** -len(clause)
        return counter

    def select_literal_JWOS(self, clauses: List[Tuple], partial_assignment: List[Tuple]):
        counter = self.get_literal_occurances(clauses, partial_assignment)
        return max(counter, key=counter.get)

    def select_literal_JWTS(self, clauses: List[Tuple], partial_assignment: List[Tuple]):
        counter = self.get_literal_occurances(clauses, partial_assignment)
        variable_counter = {}
        for variable in self.variables_set:
            variable_counter[variable] = [counter.get((variable, True), 0), counter.get((variable, False), 0)]
        max_sum_variable = max(variable_counter, key=lambda k: sum(variable_counter[k]))
        if variable_counter[max_sum_variable][0] >= variable_counter[max_sum_variable][1]:
            return (max_sum_variable, True)
        else:
            return (max_sum_variable, False)

    def select_variable_fullness_based(self, clauses: List[Tuple], partial_assignment: List[Tuple]):
        already_split = set([literal[0] for literal in partial_assignment])
        if self.verbose > 4:
            print('already_split', already_split)

        available_variables = self.variables_set - already_split
        row_assignments, col_assignments = count_assignments(partial_assignment, self.sudoku_size)
        if self.verbose:
            print(f'in fullness based heuristic. \nrow\n{row_assignments}, \ncol\n{col_assignments}')

        # row_assignments = functools.reduce(operator.add, map(collections.Counter, [row_assignments, self.row_fullness]))
        # col_assignments = functools.reduce(operator.add, map(collections.Counter, [col_assignments, self.col_fullness]))
        # if self.verbose:
        #     print(f'in fullness based heuristic after adjustment. \nrow\n{row_assignments}, \ncol\n{col_assignments}')

        # Exclude already filled rows and cols
        row_assignments = {k: v for k, v in row_assignments.items() if v != 9}
        col_assignments = {k: v for k, v in col_assignments.items() if v != 9}

        max_row_key = max(row_assignments, key=row_assignments.get)
        max_col_key = max(col_assignments, key=col_assignments.get)

        if row_assignments[max_row_key] > col_assignments[max_col_key]:
            # find first digit == max_row_key in available_variables
            target_index = 0
            target_k = max_row_key
        else:
            # find second digit == max_col_key available_variables
            target_index = 1
            target_k = max_col_key

        if self.verbose:
            print('target_index', target_index, 'target_k', target_k)

        # print('Available variables', sorted(available_variables))
        for variable in available_variables:
            if variable[target_index] == str(target_k):
                if self.verbose:
                    print("Found variable based on fullness:", variable)
                return variable
        return self.select_random_variable(partial_assignment)

    def clause_simplication(self, clauses, literal: tuple):
        # copying for not to change them outside
        new_clauses = deepcopy(clauses)

        if self.verbose > 2:
            print('before simplication', new_clauses)
        # delete clauses containing true literals
        new_clauses = [c for c in new_clauses if literal not in c]
        if self.verbose > 2:
            print('simplified true literals', new_clauses)
        # shorten clauses containing false literals
        new_clauses = [[el for el in c if el != self.neg(literal)] for c in new_clauses]
        if self.verbose > 2:
            print('shortened false literals', new_clauses)

        return new_clauses

    def pure_literal_deletion(self, clauses, partial_assignment: List[Tuple]):
        used_literals = set(chain.from_iterable(clauses))
        pure_literals = {}
        for literal in used_literals:
            variable, value = literal
            if variable not in pure_literals:
                pure_literals[variable] = value
            else:
                del pure_literals[variable]

        for variable, value in pure_literals:
            pure_literal = (variable, value)
            clauses = self.clause_simplication(clauses, pure_literal)
            partial_assignment.append(pure_literal)

        return clauses, partial_assignment

    def unit_propagate(self, clauses, partial_assignment: List[Tuple]):
        # copying for not to change them outside
        clauses = deepcopy(clauses)

        unit_literal = True
        while unit_literal:
            unit_literal = None
            for clause in clauses:
                if len(clause) == 0:
                    return clauses, partial_assignment
                elif len(clause) == 1:
                    if self.verbose > 1:
                        print("found unit clause", clause)
                    unit_literal = clause[0]
                    clauses = self.clause_simplication(clauses, unit_literal)
                    partial_assignment.append(unit_literal)
                    break  # have to check the clauses from the beginning again

        return clauses, partial_assignment

    def backtrack(self, clauses, partial_assignment: List[Tuple], split_literal: tuple):
        self.backtrack_counter += 1
        # copying the list of tuples for not to change them outside
        partial_assignment = deepcopy(partial_assignment)

        if self.verbose > 2:
            print("\nBacktrack with partial_assignment", partial_assignment, 'and split_literal', split_literal)
        if split_literal != tuple():
            clauses = self.clause_simplication(clauses, split_literal)
            partial_assignment.append(split_literal)

        clauses, partial_assignment = self.unit_propagate(clauses, partial_assignment)
        clauses, partial_assignment = self.pure_literal_deletion(clauses, partial_assignment)

        # An empty set of clauses is (trivially) true (conjunction: all of these have to be true)
        if len(clauses) == 0:
            if self.verbose:
                print('Empty set of clauses')
            return True, partial_assignment

        # An empty clause is (trivially) false (disjunction: at least one of these must be true)
        if any([len(c) == 0 for c in clauses]):
            if self.verbose:
                print("Empty clause")
            return False, None

        try:
            if self.variable_selection_method == 'random':
                split_variable = self.select_random_variable(partial_assignment)
                split_literal = (split_variable, False)
            elif self.variable_selection_method == 'fullness':
                split_variable = self.select_variable_fullness_based(clauses, partial_assignment)
                split_literal = (split_variable, True)
            elif self.variable_selection_method == 'JWOS':
                split_literal = self.select_literal_JWOS(clauses, partial_assignment)
            elif self.variable_selection_method == 'JWTS':
                split_literal = self.select_literal_JWTS(clauses, partial_assignment)
        except:
            # print('Can not split anymore')
            # return False, None
            raise

        sat, assignments = self.backtrack(clauses, partial_assignment, split_literal)
        if not sat:
            if self.verbose > 2:
                print(
                    f"partial_assignment {partial_assignment} didn't work with split_literal {split_literal}. Try with negation")
            sat, assignments = self.backtrack(clauses, partial_assignment, self.neg(split_literal))

        return sat, assignments
