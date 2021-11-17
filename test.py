from itertools import chain
import math


def neg(literal):
    return (literal[0], not literal[1])

def select_MOM_variable(clauses):
    k = 2
    print(clauses)
    clauses_length = []
    variables_total = []
    for c in clauses:
        clauses_length.append(len(c))
        for e in c:
            variables_total.append(e)
    minimum_clauses = [j for j in clauses if len(j) == min(clauses_length)]
    momlist=[]
    for i in variables_total:
        occurences_positive = 0
        occurences_negative = 0
        for j in minimum_clauses:
            if i in j:
                occurences_positive += 1
            if neg(i) in j:
                occurences_negative += 1
        mom = (occurences_positive + occurences_negative) * math.pow(2, k) + occurences_positive * occurences_negative
        momlist.append(mom)
    maxmom = variables_total[momlist.index(max(momlist))]
    print(maxmom)
    return maxmom

select_MOM_variable([[('132', False),
                      ('442', False),
                      ('211', False),
                      ('333', False)],
                     [('142', False),
                      ('342', False),
                      ('321', False),
                      ('324', False)],
                     [('413', False),
                      ('131', False),
                      ('431', True),
                      ('133', True),
                      ('343', False),
                      ('242', True),
                      ('114', True),
                      ('432', False),
                      ('124', False)],
                     [('311', True),
                      ('244', False),
                      ('112', False),
                      ('341', False),
                      ('422', False),
                      ('231', False),
                      ('424', True),
                      ('121', False),
                      ('232', False)],
                     [('414', False),
                      ('433', False),
                      ('234', True),
                      ('223', False),
                      ('221', True),
                      ('411', False),
                      ('243', False),
                      ('134', False),
                      ('213', True),
                      ('334', False),
                      ('323', True),
                      ('144', False),
                      ('122', True),
                      ('412', True),
                      ('421', False),
                      ('423', False),
                      ('434', False),
                      ('314', False)],
                     [('212', False),
                      ('331', False),
                      ('312', False),
                      ('313', False),
                      ('444', False),
                      ('214', False),
                      ('344', True),
                      ('441', False),
                      ('222', False),
                      ('443', True),
                      ('143', False),
                      ('111', False),
                      ('332', True),
                      ('113', False),
                      ('241', False),
                      ('224', False),
                      ('233', False),
                      ('123', False),
                      ('141', True),
                      ('322', False)]])