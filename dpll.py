import random
from copy import deepcopy
from itertools import chain
from typing import List, Tuple


class DPLL:
    def __init__(self, clauses, variable_selection_method='random', verbose=0):
        # extracts unique variable from DIMACS format
        self.variables_set = set(map(str, (map(abs, chain.from_iterable(clauses)))))
        # converts into internal format where each literal looks like (var_name, True)
        self.clauses = [[(str(abs(literal)), literal > 0) for literal in c] for c in clauses]
        self.variable_selection_method = variable_selection_method
        self.verbose = verbose

    @staticmethod
    def neg(literal):
        return (literal[0], not literal[1])

    def select_random_variable(self, partial_assignment: List[Tuple]):
        if self.verbose:
            print('random variable selection')
            print('inside variable selection partial_assignment', partial_assignment)
        already_split = set([literal[0] for literal in partial_assignment])
        if self.verbose:
            print('already_split', already_split)
        return random.choice(list(self.variables_set - already_split))

    def select_MOM_variable(self, clauses: List[Tuple], partial_assignment):
        k = 2
        if self.verbose:
            print('MOM variable selection')
            print('inside MOM variable selection partial_assignment', partial_assignment)
        already_split = set([literal[0] for literal in partial_assignment])
        self.variables_set = self.variables_set - already_split
        k = 2
        clauses_length = []
        for c in clauses:
            clauses_length.append(len(c))
        minimum_clauses = [j for j in clauses if len(j) == min(clauses_length)]
        momlist = []
        for i in self.variables_set:
            occurences_positive = 0
            occurences_negative = 0
            for j in minimum_clauses:
                # print((str(i), True))
                # print(j)
                true_literal = (str(i), True)
                false_literal = (str(i), False)
                if true_literal in j:
                    occurences_positive += 1
                if false_literal in j:
                    occurences_negative += 1
            # print(occurences_positive)
            mom = (occurences_positive + occurences_negative) * math.pow(2,
                                                                         k) + occurences_positive * occurences_negative
            momlist.append(mom)
        maxvalue = max(momlist)
        maxmom = list(self.variables_set)[momlist.index(maxvalue)]
        self.variables_set.remove(maxmom)

        return maxmom

    def clause_simplication(self, clauses, literal: tuple):
        # copying for not to change them outside
        new_clauses = deepcopy(clauses)

        if self.verbose:
            print('before simplication', new_clauses)
        # delete clauses containing true literals
        new_clauses = [c for c in new_clauses if literal not in c]
        if self.verbose:
            print('simplified true literals', new_clauses)
        # shorten clauses containing false literals
        new_clauses = [[el for el in c if el != self.neg(literal)] for c in new_clauses]
        if self.verbose:
            print('shortened false literals', new_clauses)

        return new_clauses

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
                    if self.verbose:
                        print("found unit clause", clause)
                    unit_literal = clause[0]
                    clauses = self.clause_simplication(clauses, unit_literal)
                    partial_assignment.append(unit_literal)
                    break  # have to check the clauses from the beginning again

        return clauses, partial_assignment

    def backtrack(self, clauses, partial_assignment: List[Tuple], split_literal: tuple):
        # copying the list of tuples for not to change them outside
        partial_assignment = deepcopy(partial_assignment)

        if self.verbose:
            print("\nBacktrack with partial_assignment", partial_assignment, 'and split_literal', split_literal)
        if split_literal != tuple():
            clauses = self.clause_simplication(clauses, split_literal)
            partial_assignment.append(split_literal)

        clauses, partial_assignment = self.unit_propagate(clauses, partial_assignment)

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
        except:
            print('Can not split anymore')
            return False, None
        split_literal = (split_variable, False)
        sat, assignments = self.backtrack(clauses, partial_assignment, split_literal)
        if not sat:
            if self.verbose:
                print(
                    f"partial_assignment {partial_assignment} didn't work with split_literal {split_literal}. Try with negation")
            sat, assignments = self.backtrack(clauses, partial_assignment, self.neg(split_literal))

        return sat, assignments
