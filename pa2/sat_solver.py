"""
PA2: SAT solver for CNF formulas.

A clause is a list of integers.
Example:
[1, -3, 4] means x1 OR not x3 OR x4.

An assignment is a dictionary where:
key = variable number
value = True or False
"""

import ast
import sys


def get_var(lit):
    return abs(lit)     # The variable is always the positive version of the literal.


def value_needed(lit):
    return lit > 0          # Positive literals need True, negative literals need False.


def eval_lit(lit, assignment):
    var = get_var(lit)          # Checks if one literal is true, false, or not decided yet.
    if var not in assignment:
        return None
    return assignment[var] == value_needed(lit)


def simplify(clauses, assignment):     # Removes clauses that are already true -- Removes literals that are already false.
    new_clauses = []
    for clause in clauses:
        new_clause = []
        clause_is_true = False
        for lit in clause:
            result = eval_lit(lit, assignment)
            if result is True:
                clause_is_true = True
                break
            if result is None:
                new_clause.append(lit)
        if clause_is_true:
            continue
        if len(new_clause) == 0:         # Empty clause means this path cannot work.
            return None
        new_clauses.append(new_clause)
    return new_clauses


def unit_propagate(clauses, assignment):
    clauses = simplify(clauses, assignment)     # If a clause has only one literal, that literal must be true
    if clauses is None:
        return None
    while True:
        unit_lit = None
        for clause in clauses:
            if len(clause) == 1:
                unit_lit = clause[0]
                break
        if unit_lit is None:
            return clauses

        assignment[get_var(unit_lit)] = value_needed(unit_lit)
        clauses = simplify(clauses, assignment)
        if clauses is None:
            return None


def choose_variable(clauses, assignment):     # Just pick the first variable that has not been assigned yet
    for clause in clauses:
        for lit in clause:
            var = get_var(lit)
            if var not in assignment:
                return var
    return None


def sat_solve(clauses, assignment):      # Make a copy so we do not mess up the old assignment
    assignment = dict(assignment)
    clauses = unit_propagate(clauses, assignment)

    if clauses is None:     # This branch failed.
        return None

    if len(clauses) == 0:      # No clauses left means everything is satisfied.
        return assignment

    var = choose_variable(clauses, assignment)

    # First try setting the variable to True.
    true_assignment = dict(assignment)
    true_assignment[var] = True
    result = sat_solve(clauses, true_assignment)
    if result is not None:
        return result

    # If True did not work, try False.
    false_assignment = dict(assignment)
    false_assignment[var] = False
    return sat_solve(clauses, false_assignment)


def print_result(assignment):
    print(f"satisfiable: {str(assignment is not None).lower()}")
    print(f"assignment: {assignment}")


def main():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read()

    clauses = ast.literal_eval(raw)
    answer = sat_solve(clauses, {})

    print_result(answer)

if __name__ == "__main__":
    main()