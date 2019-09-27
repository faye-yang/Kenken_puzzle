#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

from cspbase import *
import itertools


def make_row_cons(variables, curr_var, r, c):
    row_cons= []
    row = variables[r]
    for i in range(0, len(row)):
        if i <= c:
            continue
        else:
            domains = []
            domains.append(curr_var.domain())
            domains.append(row[i].domain())
            sat_tuples = []

            for t in itertools.product(*domains):
                if t[0] != t[1]:
                    sat_tuples.append(t)
            con = Constraint("C:V{}{}V{}{}".
                format(r+1, c+1, r+1, i+1), [curr_var, row[i]])
            con.add_satisfying_tuples(sat_tuples)
            row_cons.append(con)

    return row_cons


def make_col_cons(variables, curr_var, r, c):
    cons = []
    vars = []
    for row in variables:
        vars.append(row[c])

    for i in range(len(vars)):
        if i <= r:
            continue
        else:
            domains = []
            domains.append(curr_var.domain())
            domains.append(vars[i].domain())
            sat_tuples = []

            for t in itertools.product(*domains):
                if t[0] != t[1]:

                    sat_tuples.append(t)
            con = Constraint("C:V{}{}V{}{}".
                format(r+1, c+1, i+1, c+1), [curr_var, vars[i]])
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    return cons


def binary_ne_grid(kenken_grid):
    ##IMPLEMENT
    size = kenken_grid[0][0]
    dom=[]
    cons = []

    for num in range(1,size+1):
        dom.append(num)

    #initialized all variables
    vars=[]
    for row in range(1,size+1):
        rowL =[]
        for column in range(1,size+1):
            rowL.append(Variable("V{}{}".
                format(row, column),dom))
        vars.append(rowL)
    n=len(kenken_grid)
    constraint=1
    while constraint<n:
        if len(kenken_grid[constraint])==2:
            cell=kenken_grid[constraint][0]
            target=kenken_grid[constraint][1]
            for value in dom:
                if value != target:
                    vars[cell[0]][cell[1]].prune_value(value)
        constraint+=1
    for i in range(0, len(vars)):
        row = vars[i]
        for j in range(len(row)):
            curr_var = row[j]
            row_cons = make_row_cons(vars, curr_var, i, j)
            col_cons = make_col_cons(vars, curr_var, i, j)
            cons.extend(row_cons)
            cons.extend(col_cons)

    kenken_csp = CSP("kenkencsp:size{}".format(size))

    #add variables
    for row in vars:
        for v in row:
            kenken_csp.add_var(v)

    #add constraints
    for each_con in cons:
        kenken_csp.add_constraint(each_con)

    return kenken_csp, vars


def nary_ad_grid(kenken_grid):
    ##IMPLEMENT
    size = kenken_grid[0][0]
    dom = []
    for i in range(1, size + 1):
        dom.append(i)

    # initialized all variables
    vars = []
    for row in range(1, size + 1):
        rowL = []
        for column in range(1, size + 1):
            rowL.append(Variable("V{}{}".
                                 format(row, column), dom))

        vars.append(rowL)
    n = len(kenken_grid)
    constraint = 1
    while constraint < n:
        if len(kenken_grid[constraint]) == 2:
            cell = kenken_grid[constraint][0]
            target = kenken_grid[constraint][1]
            for value in dom:
                if value != target:
                    vars[cell[0]][cell[1]].prune_value(value)
        constraint += 1
    cons=[]
    #row constraint
    for row_num in range(len(vars)):
        #each row add domain
        domains = []
        sat_tuples = []
        for var in vars[row_num]:
            domains.append(var.domain())

        for t in itertools.product(*domains):
            if len(set(t)) == len(t):
                sat_tuples.append(t)

        con = Constraint("C:R{}".
                         format(row_num), vars[row_num])

        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    #add column constraint
    for col_num in range(len(vars)):
        col_list=[item[col_num] for item in vars]
        domains = []
        sat_tuples = []
        for var in col_list:
            domains.append(var.domain())
        for t in itertools.product(*domains):
            if len(set(t)) == len(t):
                sat_tuples.append(t)

        con = Constraint("C:C{}".
                         format(col_num), col_list)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
    kenken_csp = CSP("kenken:size{}".format(size))

    # add variables
    for row in vars:
        for v in row:
            kenken_csp.add_var(v)

    # add constraints
    for each_con in cons:
        kenken_csp.add_constraint(each_con)
    return kenken_csp, vars


def kenken_csp_model(kenken_grid):
    ##IMPLEMENT
    size = kenken_grid[0][0]
    #add binary constraint
    kenken_csp, vars=binary_ne_grid(kenken_grid)
    cons = []

    # add kenken constraints
    for i in range(1, len(kenken_grid)):
        cage = kenken_grid[i]
        cage_size=len(cage)
        scope = []
        varDoms = []
        for j in range(0, len(cage) - 2):
            each_dom = []
            for k in range(1, size + 1):
                each_dom.append(k)
            varDoms.append(each_dom)
            index1 = int(str(cage[j])[0])
            index2 = int(str(cage[j])[1])
            scope.append(vars[index1 - 1][index2 - 1])
        sat_tuples = []
        for t in itertools.product(*varDoms):
            if cage_size > 2:
                if cage_constraint(t, cage[cage_size - 2], cage[cage_size - 1]):
                    sat_tuples.append(t)
            else:
                if t[0] == cage[cage_size - 1] :
                    sat_tuples.append(t)
        # make con
        con = Constraint("C:cage{})".format(i), scope)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # add all constraints
    for each_con in cons:
        kenken_csp.add_constraint(each_con)

    return kenken_csp, vars




def cage_constraint(t, result, operator):
    #sum
    if operator == 0:
        if sum(t) == result:
            return True
        return False
    elif operator == 1:
        for perms in itertools.permutations(t):
            curr_result = perms[0]-sum(perms[1:])
            if curr_result == result:
                return True
        return False
    elif operator == 2:
        for perms in itertools.permutations(t):
            curr_result = perms[0]
            for i in perms[1:]:
                curr_result = curr_result/i
            if curr_result == result:
                return True
        return False
    elif operator == 3:
        product = 1
        for num in t:
            product = product * num
        if product == result:
            return True
        return False
