import itertools
from copy import deepcopy

def negate_atom(alpha):
    if alpha.startswith('-'):
        return alpha.replace('-', '')
    return str('-' + alpha)

def negate_clause(clause):
    res = list()
    for lit in clause:
        res.append(negate_atom(lit))
    return res

def negative_remove_lit(clause):
    for lit in clause:
        #print(f'lit: {type(lit)}')
        negated_lit = negate_atom(lit)
        #print(f'negated lit: {negated_lit}')
        if negated_lit in clause:
            #print("YES")
            clause.remove(negated_lit)
            clause.remove(lit)
    return clause

def negative_remove_clause(clauses):
    res = []
    for clause in clauses:
        res.append( negative_remove_lit(clause) )
    return res

def duplicate_remove_lit(clause):
    res = set()
    for lit in clause:
        if lit not in res:
            res.add(lit)
    return list(res) 

def duplicate_remove_clause(clauses):
    res = []
    for clause in clauses:
        cleaned = duplicate_remove_lit(clause)
        if cleaned not in res:
            res.append(cleaned)
    return res    

def clauses_cleaned(clauses):
    clauses = duplicate_remove_clause(clauses)
    clauses = negative_remove_clause(clauses)
    return clauses
    
def lit_cleaned(lit):
    lit = negative_remove_lit(lit)
    lit = duplicate_remove_lit(lit)
    lit = sorted(set(lit), key=lambda x: (x.lstrip('-'), x.startswith('-')))
    return lit

def resolved(clause_i, clause_j):
    new_clause = []
    for lit in clause_i:
        negated_lit = negate_atom(lit)
        if negated_lit in clause_j:
            temp_c_i = clause_i.copy()
            temp_c_j = clause_j.copy()
            temp_c_i.remove(lit)
            temp_c_j.remove(negated_lit)
            combined_clause = temp_c_i + temp_c_j
            cleaned_clause = lit_cleaned(combined_clause)
            if cleaned_clause and cleaned_clause not in new_clause:
                new_clause.append(cleaned_clause)
            elif not cleaned_clause:
                new_clause.append(['{}'])
    return new_clause
            
def PL_resolution_ouput(alpha, KB, filepath):
    tempKB = deepcopy(KB)
    negated_alpha = negate_clause(alpha)
    
    for lit in negated_alpha:
        tempKB.append([lit])

    with open(filepath, "w") as output_file:
        iteration = 1
        
        while True:
            clause_pairs = list(itertools.combinations(tempKB, 2))
            generated_clauses = []
            print(f"The run {iteration}:")
            for (clause_i, clause_j) in clause_pairs:
                resolvents = resolved(clause_i, clause_j)
                
                for clause in resolvents:
                    if clause not in tempKB and clause not in generated_clauses:
                        generated_clauses.append(clause)
                        
                        print('-------------------------------------------------------')
                        print(f"{clause_i} + {clause_j} => {clause}")

            output_file.write(f"{len(generated_clauses)}\n")
            for clause in generated_clauses:
                output_file.write(f"{' OR '.join(clause) if clause != ['{}'] else '{}'}\n")

            if ['{}'] in generated_clauses:
                output_file.write("YES\n")
                return True

            if not generated_clauses:
                output_file.write("NO\n")
                return False

            tempKB.extend(generated_clauses)
            
            iteration += 1