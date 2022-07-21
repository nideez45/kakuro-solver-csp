from itertools import permutations
from collections import deque
import copy
import kakuro


l = list(permutations(range(1,10)))
def perm(length,sum_needed):
    if length == 1:
        return [sum_needed]
    possible = set()
    for tup in l:
            temp = list(tup)
            if sum(temp[0:length]) == sum_needed:
                possible.add(tup[0:length])
    possible = list(possible)
    return possible

singlevariable = {}

variables = set()
unassigned_variable = []
neighbours = {}
assignment = {}
domain = {}
constraint = {}

row_constraints = kakuro.row_constraint
col_constraints = kakuro.colum_constraint
row_sums = kakuro.row_sum
col_sums = kakuro.colum_sum

for row_constraint in row_constraints:
    for var in row_constraint:
        variables.add(var)
for col_constraint in col_constraints:
    for var in col_constraint:
        variables.add(var)

for row_constraint in row_constraints:
    for var in row_constraint:
        neighbours[var] = [];
        for neighbour in row_constraint:
            if var != neighbour:
                neighbours[var].append(neighbour)
for col_constraint in col_constraints:
    for var in col_constraint:
        if var not in neighbours.keys():
            neighbours[var]=[]
        for neighbour in col_constraint:
            if var != neighbour:
                neighbours[var].append(neighbour)
i=0
for row_constraint in row_constraints:
    for var in row_constraint:
        domain[var] = []
        for val in range(1,min(row_sums[i]+1,10)):
            domain[var].append(val)
    i+=1
i=0
for col_constraint in col_constraints:
    for var in col_constraint:
        if var not in domain.keys():
            domain[var] = []
            for val in range(1,col_sums[i]+1):
                domain[var].append(val)
        else:
            lst = domain[var][-1]
            x = min(9,col_sums[i])
            if lst>x:
                while domain[var][-1] >x:
                    domain[var].pop()
    i+=1


c1 = []
c2 = []
i=0
for row_constraint in row_constraints:
    if len(row_constraint) == 1:
        singlevariable[row_constraint[0]] = row_sums[i]
    c = perm(len(row_constraint),row_sums[i])
    i+=1
    c1.append(c)

i=0
for col_constraint in col_constraints:
    if len(col_constraint) == 1:
        singlevariable[col_constraint[0]] = col_sums[i]
    c = perm(len(col_constraint),col_sums[i])
    i+=1
    c2.append(c)

for k in range(len(c1)):
    for possible_assigment in c1[k]:
        for i in range(len(row_constraints[k])):
            for j in range(len(row_constraints[k])):
                if i != j:
                    constraint[(row_constraints[k][i],possible_assigment[i],row_constraints[k][j],possible_assigment[j])] = 1
  
for k in range(len(c2)):
    for possible_assigment in c2[k]:
        for i in range(len(col_constraints[k])):
            for j in range(len(col_constraints[k])):
                if i != j:
                    constraint[(col_constraints[k][i],possible_assigment[i],col_constraints[k][j],possible_assigment[j])]=1;

unassigned_variable = list(variables)
"""
print("Row constraints")
print(row_constraints)
print("Row sum")
print(row_sums)
print("Col constraints")
print(col_constraints)
print("Col sum")
print(col_sums)"""

def remove_inconsistent_values(Xi,Xj,domain):
    ok = False
    toremove = []
    for value1 in domain[Xi]:
        cnt=0
        for value2 in domain[Xj]:
            if (Xi,value1,Xj,value2) in constraint.keys():
                cnt+=1
        if cnt == 0:
            ok = True
            toremove.append(value1)
    for val in toremove:
        domain[Xi].remove(val)
    return ok


def ac3(variables,constraint,domain):
    q = deque()
    for var in variables:
        if var not in singlevariable.keys():
            for neighbour in neighbours[var]:
                q.append([var,neighbour])
    while len(q):
        [Xi,Xj] = q.popleft()
        if remove_inconsistent_values(Xi,Xj,domain):
            for neighbour in neighbours[Xi]:
                q.append([neighbour,Xi])
    return domain

domain = ac3(variables,constraint,domain)

def remove_inconsistent_values_ac3(Xi,Xj,domain,assignment):
    toremove = []
    result = False
    for value1 in domain[Xi]:
        cnt=0
        for value2 in domain[Xj]:
            if Xj in assignment.keys():
                value2 = assignment[Xj]
        
            if (Xi,value1,Xj,value2) in constraint.keys():
                cnt+=1
        if cnt == 0:
            result = True
            toremove.append(value1)
    for val in toremove:
        domain[Xi].remove(val)
    
    return [domain,result]
        
def ac3_mac(var,constraint,domain,assignment):
    q = deque()
    for neighbour in neighbours[var]:
        if neighbour not in assignment.keys():
            q.append([neighbour,var])
    newdomain = copy.deepcopy(domain)
    while len(q):
        [Xi,Xj] = q.popleft()
        newdomain,result = remove_inconsistent_values_ac3(Xi,Xj,newdomain,assignment)
        if len(newdomain[Xi]) == 0:
            return newdomain,False
        if result:
            for neighbour in neighbours[Xi]:
                q.append([neighbour,Xi])
    return newdomain,True
cnt = 0

# backtracking search with MAC (maintaining arc consistency)

def bs_mac(assignment,constraint,domain,unassigned_variable):
    global cnt
    cnt+=1
    if len(assignment) == len(variables):
        return assignment
    if len(unassigned_variable):
        var = unassigned_variable[-1]
       
        for value in domain[var]:
            ok = True
            for var1 in neighbours[var]:
                if var1 in assignment.keys():
                    constraint1 = (var,value,var1,assignment[var1])
                    if constraint1 not in constraint.keys():
                        ok = False
        
            if ok:
                unassigned_variable.pop()
                assignment[var] = value
               
                if var in singlevariable.keys():
                    assignment[var] = singlevariable[var]
                
                saved_domain={}
                for var1 in list(variables):
                    saved_domain[var1] = domain[var1]
                domain,valid = ac3_mac(var,constraint,domain,assignment)
                if valid:
                    result = bs_mac(assignment,constraint,domain,unassigned_variable)
                    if result != False:
                        return assignment
                    else:
                        assignment.pop(var)
                        unassigned_variable.append(var)
                else:
                    assignment.pop(var)
                    unassigned_variable.append(var)
                domain = {}
                for var1 in list(variables):
                    domain[var1] = saved_domain[var1]
        
        return False

answer = bs_mac({},constraint,domain,unassigned_variable)
print(cnt)
print(answer)
