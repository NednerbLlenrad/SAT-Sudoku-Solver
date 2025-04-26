# main.py  (project root)
from Sudoku_Generator import run                  #  ← use the helper
from Z3_IO.z3_io  import sudoku_to_cnf, cnf_to_sudoku
from z3solver     import solve_cnf

# 1. build a 9×9 puzzle
board = run(3)               # run(block_size) does all the filling & digging
grid  = board.grid

print("Initial puzzle:")
for row in grid:
    print(*row)

# 2. encode to CNF
N   = len(grid)
cnf = sudoku_to_cnf(grid, N)

# 3. solve with Z3
model = solve_cnf(cnf)
if model is None:
    print("UNSAT — puzzle has no solution")
    exit()

# 4. convert model → solved grid
solved = cnf_to_sudoku(model, N)

print("\nSolved puzzle:")
for row in solved:
    print(*row)
