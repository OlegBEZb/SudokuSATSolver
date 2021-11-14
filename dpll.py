import random
from copy import deepcopy

class DPLL:
    def __init__(self, clauses, nvars, variable_selection_method='random'):
        self.clauses = clauses
        self.variables_set = set([i+1 for i in range(nvars)])  # TODO: get variables set
        self.variable_selection_method = variable_selection_method

    # def try_solution(self, clauses, partial_assignment):
    #     pass
    #     # for clause in clauses:

    def select_random_variable(self, partial_assignment: tuple):
        return random.choice(list(self.variables_set - set([abs(v) for v in partial_assignment])))

    def clause_simplication(self, clauses, literal: int):
        new_clauses = deepcopy(clauses)
        print('before simplication', new_clauses)
        # delete clauses containing true literals
        new_clauses = [c for c in new_clauses if literal not in c]
        print('simplified true literals', new_clauses)
        # shorten clauses containing false literals
        new_clauses = [[el for el in c if el != ((-1)*literal)] for c in new_clauses]
        print('shortened false literals', new_clauses)

        return new_clauses

    def backtrack(self, clauses, partial_assignment: tuple = tuple(), split_variable: int = None):
        # An empty set of clauses is (trivially) true (conjunction: all of these have to be true)
        if len(clauses) == 0:
            return True, partial_assignment

        # An empty clause is (trivially) false (disjunction: at least one of these must be true)
        if any([len(c) == 0 for c in clauses]):
            return False, None

        # partial_assignment_result = self.try_solution(partial_assignment)

        if self.variable_selection_method == 'random':
            split_variable = self.select_random_variable(partial_assignment)

        print('\npartial_assignment', partial_assignment, 'split_variable', split_variable)
        clauses = self.clause_simplication(clauses, split_variable)
        partial_assignment = partial_assignment + (split_variable,)

        sat, assignments = self.backtrack(clauses, partial_assignment, split_variable)
        if not sat:
            sat, assignments = self.backtrack(clauses, partial_assignment, -split_variable)

        return sat, assignments
