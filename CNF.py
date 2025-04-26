import itertools

def var(i, j, k, n=9):
    """
    Map (row i, column j, number k) to a unique SAT variable number (starting from 1).
    i, j, k are 0-based (0 to 8).
    """
    return i * n * n + j * n + k + 1

def generate_sudoku_cnf(n=9):
    clauses = []
    v       = var             # Optimized: local alias to avoid global look‑up
    rng     = range(n)        # Optimized: reuse the same range object
    extend  = clauses.extend  # Optimized: batch insert instead of many append calls

    # Each cell must have at least one number
    extend([[v(i, j, k, n) for k in rng]          # Optimized: list‑comp + extend
            for i in rng for j in rng])

    # Each cell must have at most one number (no two numbers in one cell)
    for i in rng:
        for j in rng:
            extend([[-v(i, j, k1, n), -v(i, j, k2, n)]
                    for k1, k2 in itertools.combinations(rng, 2)])

    # Each number must appear exactly once in each row
    for i in rng:
        for k in rng:
            row_vars = [v(i, j, k, n) for j in rng]
            clauses.append(row_vars)
            extend([[-row_vars[j1], -row_vars[j2]]
                    for j1, j2 in itertools.combinations(rng, 2)])

    # Each number must appear exactly once in each column
    for j in rng:
        for k in rng:
            col_vars = [v(i, j, k, n) for i in rng]
            clauses.append(col_vars)
            extend([[-col_vars[i1], -col_vars[i2]]
                    for i1, i2 in itertools.combinations(rng, 2)])

    # Each number must appear exactly once in each 3x3 subgrid
    block_size = int(n ** 0.5)
    assert block_size * block_size == n, "n must be a perfect square (like 9)."

    for k in rng:
        for block_row in range(0, n, block_size):
            for block_col in range(0, n, block_size):
                block_vars = [v(block_row + dr, block_col + dc, k, n)
                              for dr in range(block_size) for dc in range(block_size)]
                clauses.append(block_vars)
                extend([[-c1, -c2] for c1, c2 in itertools.combinations(block_vars, 2)])

    return clauses

def save_cnf(clauses, filename="sudoku_9x9.cnf", n=9):
    num_vars = n * n * n
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

if __name__ == "__main__":
    cnf_clauses = generate_sudoku_cnf(n=9)
    save_cnf(cnf_clauses, filename="sudoku_9x9.cnf", n=9)
    print(" CNF file generated: sudoku_9x9.cnf")
