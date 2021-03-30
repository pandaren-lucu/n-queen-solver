import os

def generate_sat(n):
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
            diagonals[i - j].append((n * i) + j + 1)
    
    for diagonal in diagonals:
        if len(diagonal) > 1:
            for i in range(len(diagonal)):
                for j in range(j + 1, len(diagonal)):
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
                for j in range(j + 1, len(diagonal)):
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

def write_sat_clauses_to_file(n, sat_clauses, file_path = None):
    if not file_path:
        file_path = "minisat.in"
    else:
        file_path = os.path.join(file_path, "minisat.in")
    
    with open(file_path, "w+") as minisat_input_file:
        minisat_input_file.write("p cnf {} {}\n".format(n, len(sat_clauses)))
        for clause in sat_clauses:
            string_clause = " ".join([str(var) for var in clause]) + " 0\n"
            minisat_input_file.write(string_clause)
        minisat_input_file.close()