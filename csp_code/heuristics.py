#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
from collections import defaultdict

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    #IMPLEMENT
    variables=csp.get_all_unasgn_vars()
    min_d=10000
    min_v=None
    if variables==[]:
        return None
    for i in variables:
        n=i.cur_domain_size()
        if n <  min_d:
            min_d=n
            min_v=i
    return min_v


def val_lcv(csp,var):
    #IMPLEMENT
    valueNum=[]
    domain_const=defaultdict(int)
    if var==None:
        return valueNum
    else:
        cons=csp.get_cons_with_var(var)
    curDom=var.cur_domain()
    for constraint in cons:
        for i in curDom:
            if (var, i) in constraint.sup_tuples:
                for t in constraint.sup_tuples[(var, i)]:
                    if constraint.tuple_is_valid(t):
                        domain_const[i]+=1

    sorted(domain_const.items(), key = lambda x : x[1])
    for key in domain_const:
        valueNum.append(key)
    return valueNum




