import os
import sys
from subprocess import call

def generate_n_queen_clauses(n):
    sat_clauses = []
    # Generate clauses for rule "Only one queen per row"
    for i in range(1, (n * n) + 1):
        if (i % n) != 0:
            for j in range(i + 1, i + 1 + (n - (i % n))):
                clause = [-i, -j]
                sat_clauses.append(clause)
    
    # Generate clauses for rule "Only one queen per column"
    for i in range(1, (n * n) + 1):
        for j in range (i + n, (n * n) + 1, n):
            clause = [-i, -j]
            sat_clauses.append(clause)
    
    # Generate clauses for rule "Only one queen in a top-left to bottom-right diagonal"
    diagonals = [[] for i in range(n + n + 1)]
    for i in range(n):
        for j in range(n):
            diagonals[i - j + n - 1].append((n * i) + j + 1)
    
    for diagonal in diagonals:
        if len(diagonal) > 1:
            for i in range(len(diagonal)):
                for j in range(i + 1, len(diagonal)):
                    clause = [-diagonal[i], -diagonal[j]]
                    sat_clauses.append(clause)

    # Generate clauses for rule "Only one queen in a top-right to bottom-left diagonal"
    diagonals = [[] for i in range(n + n + 1)]
    for i in range(n):
        for j in range(n):
            diagonals[i + j].append((n * i) + j + 1)
    
    for diagonal in diagonals:
        if len(diagonal) > 1:
            for i in range(len(diagonal)):
                for j in range(i + 1, len(diagonal)):
                    clause = [-diagonal[i], -diagonal[j]]
                    sat_clauses.append(clause)

    # Generate clauses for rule "There must be at least one queen in a row"
    for i in range(1, (n * n) + 1, n):
        clause = []
        for j in range(i, i + n):
            clause.append(j)
        sat_clauses.append(clause)

    # Generate clauses for rule "There must be at least one queen in a column"
    for i in range(1, n + 1):
        clause = []
        for j in range(i, (n * n) + 1, n):
            clause.append(j)
        sat_clauses.append(clause)
    
    return sat_clauses

def solve_n_queen(n, sat_clauses):
    """
    Solve an N-Queen SAT problem using minisat.
    
    Takes input n denoting length of the board and sat_clauses is a list of list containing clauses in minisat format.
    Ex: (2, [[1, -2], [1, 2]]) is a N-Queen SAT problem with length of the board is 2 and containing clauses
    (-(X1 or not X2) and (X1 or X2))

    Return (bool error, bool is_sat, list sat_vars_value)
    error: if there is an error occurs during the solving process
    is_sat: satisfiability of the problem
    sat_vars_value: list of SAT variable value that satisfy the problem if the problem is satisfiable
    and an empty list if the problem is unsatisfiable.

    WARNING: Make sure that minisat is already added to terminal path and can be called without using explicit path.
    """
    input_file_path = "minisat.in"
    output_file_path = "minisat.out"
    
    # Creating input file
    with open(input_file_path, "w+") as minisat_input_file:
        minisat_input_file.write("p cnf {} {}\n".format(n * n, len(sat_clauses)))
        for clause in sat_clauses:
            string_clause = " ".join([str(var) for var in clause]) + " 0\n"
            minisat_input_file.write(string_clause)

    command = 'minisat %s %s > ' + ('NUL' if sys.platform == 'win32' else '/dev/null')
    command = command % (input_file_path, output_file_path)

    return_code = call(command, shell=True)

    if return_code != 10:
        return (False, None, [])

    with open(output_file_path, "r") as minisat_output_file:
        lines = minisat_output_file.readlines()
        
        is_sat = lines[0].startswith("SAT")

        if not is_sat:
            return [False, False, []]

        sat_vars_value = []
        var_lines = lines[1:]
        for var_line in var_lines:
            sat_vars = var_line.split(" ")[:-1]
            for sat_var in sat_vars:
                sat_vars_value.append(int(sat_var))
        
        return [False, True, sat_vars_value]