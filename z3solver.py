from z3 import Solver, Bool, Or, Not, sat

def solve_cnf(cnf):
    """
    Solves a SAT problem given in CNF form using Z3.
    
    Args:
        cnf (list[list[int]]): CNF formula where each clause is a list of integers.
                               A positive integer i represents variable v_i,
                               and a negative integer -i represents Not(v_i).
    
    Returns:
        dict or None: A dictionary mapping variable names to Boolean values if satisfiable, else None.
    """
    # Determine the maximum variable index in the CNF
    max_var = max(abs(lit) for clause in cnf for lit in clause)
    # Create Boolean variables v1, v2, ..., v_max
    variables = {i: Bool(f"v{i}") for i in range(1, max_var + 1)}
    
    solver = Solver()
    
    # Add each clause to the solver
    for clause in cnf:
        # Convert the clause into a Z3 OR expression
        z3_clause = []
        for lit in clause:
            if lit > 0:
                z3_clause.append(variables[lit])
            else:
                z3_clause.append(Not(variables[abs(lit)]))
        solver.add(Or(z3_clause))
    
    # Check if the CNF is satisfiable
    if solver.check() == sat:
        model = solver.model()
        # Create an assignment dictionary
        assignment = {str(variables[i]): model.evaluate(variables[i]) for i in variables}
        return assignment
    else:
        return None

# Example usage:
if __name__ == "__main__":
    # Example CNF: (v1 or not v2) and (not v1 or v3 or v2)
    example_cnf = [
        [1, -2],
        [-1, 3, 2]
    ]
    
    solution = solve_cnf(example_cnf)
    if solution:
        print("SAT solution found:")
        for var, val in solution.items():
            print(f"{var} = {val}")
    else:
        print("The CNF is unsatisfiable.")
