from pysat.solvers import Minisat22

def solve_cnf(cnf):
    norm = []
    for cl in cnf:
        # Turn unit–clauses (ints) into 1‑element lists,
        # and coerce every literal to int
        if isinstance(cl, (list, tuple)):
            norm.append([int(l) for l in cl])
        else:
            norm.append([int(cl)])
    # Now every clause in `norm` is a List[int].
    with Minisat22(bootstrap_with=norm) as solver:
        if not solver.solve():
            return None
        model = solver.get_model()
    return {f"v{abs(lit)}": lit > 0 for lit in model}
