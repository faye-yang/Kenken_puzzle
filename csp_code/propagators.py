#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())

            if not c.check(vals):
                return False, []
    return True, []


def FC_check(C,x):
    ''' C: the constraint with  all its variables already assigned x: variable that is not assigned'''
    cur_Dom=x.cur_domain()
    prune=[]
    for i in cur_Dom:
        value =[]
        variables=C.get_scope()

        for v in variables:
            if v.is_assigned():
                value.append(v.get_assigned_value())
            else:
                value.append(i)

        if not C.check(value):
            x.prune_value(i)
            prune.append((x,i))
    if x.cur_domain() ==[]:
        return True,prune
    else:
        return False,prune


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    pruned=[]
    if newVar==None:
        cons=csp.get_all_cons()
    else:
        cons=csp.get_cons_with_var(newVar)
    for constraint in cons:
        if constraint.get_n_unasgn() ==1:
            vars = constraint.get_unasgn_vars()
            last_unasgn_var = vars[0]
            check,prune=FC_check(constraint,last_unasgn_var)
            pruned.extend(prune)
            if check:
                return False,pruned
    return True,pruned



#GAC enforce
def enforce_GAC(GAC_queue,csp):
    prune=[]
    while GAC_queue != []:
        cons=GAC_queue.pop()
        for variable in cons.get_scope():
            for d in variable.cur_domain():
                if cons.has_support(variable,d):
                    continue
                else:
                    #remove the value
                    variable.prune_value(d)
                    prune.append((variable, d))
                    if variable.cur_domain_size() == 0:
                        GAC_queue.clear()
                        return False, prune
                    else:
                        #add all constraint that contain that variable that satisfy back to gac queue.
                        cons_related=csp.get_cons_with_var(variable)
                        for c in cons_related:
                            if c not in GAC_queue:
                                GAC_queue.append(c)
    return True,prune




def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    cons = []
    if (newVar != None):
        cons.extend(csp.get_cons_with_var(newVar))
    else:
        cons.extend(csp.get_all_cons())
    GACqueue = []
    GACqueue.extend(cons)
    check,prune=enforce_GAC(GACqueue,csp)
    return check, prune

#IMPLEMENT
