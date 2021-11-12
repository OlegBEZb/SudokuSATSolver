import random


def readinsudokurules():
    totalrules= filetolist('sudoku-rules.txt')
    p = totalrules[0][1]
    cnf = totalrules[0][2]
    totalrules.pop(0)

    return totalrules

def readinsudoku(sudokuname):
    rules=readinsudokurules()
    sudoku=filetolist(sudokuname)
    rules+= sudoku
    rules = [[int(float(j)) for j in i] for i in rules]


    return rules


def filetolist(filename):
    file = open(filename)
    file = file.readlines()
    list = []
    for i in file:
        rule = i.split()
        list.append(rule)

    return list




# def SATsolver():
#     DIMACSexample = [[-1,2,3,-4,5],[1,2,3,4,-5],[2,-5],[-1,-4]]
#     #split
#     totalvariables = []
#     for i in DIMACSexample:
#         for j in i:
#             if j <0:
#                 j= j*-1
#                 totalvariables.append(j)
#             else:
#                 totalvariables.append(j)
#     totalvariables=list(dict.fromkeys(totalvariables))
#     print(totalvariables)
#     split(DIMACSexample,totalvariables,solution=[])


# def split(checkingset, totalvariables, solution,indentation):
#
#     while check(checkingset, solution,):
#         split = random.choice(totalvariables)
#         totalvariables.remove(split)
#         solution.append(split)
#
#         if len(solution) == len(totalvariables):
#             print('solution= ',solution)
#             break
#         # backtrack
#
#     else:
#
#         solution[indentation]=solution[indentation]*-1
#         indentation=indentation-1
#         split(checkingset,totalvariables,solution)
#     print(solution)

def check():
    checkingset = [[1,2,3],[1,-2],[1,-3],[-1,3]]
    solution = [-1,2,3]

    for i in checkingset:
        #invert the checkingset to check solutions
        invertedexample = []
        for j in i:
            j = j*-1
            invertedexample.append(j)
        #check if values of solution are in checkingset else they dont have to check anything
        if list(set(invertedexample)&set(solution)) or list(set(i)&set(solution)):
            #if invertedset-solution has no values it is false
            if not list(set(invertedexample)-set(solution)):
                return False
    return True




readinsudoku('sudoku-example.txt')
print(check())

