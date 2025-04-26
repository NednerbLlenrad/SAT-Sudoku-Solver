import tksheet
from tksheet import Sheet
import tkinter as tk
import BoardGenerator.SudokuBoard as Sudoku_Generator
import CNF
from Z3_IO.z3_io import sudoku_to_cnf, cnf_to_sudoku
import z3solver
import pysat_solver
import time

root = tk.Tk()
root.title("Sudoku Solver")

input_frame = tk.Frame(root)
input_frame.pack()

selected_difficulty = tk.StringVar()
selected_difficulty.set("Hard")
difficulty_levels = ["Easy", "Medium", "Hard"]

selected_solver = tk.StringVar()
selected_solver.set("Z3")
solvers = ["Z3", "PySAT"]

boardsize = tk.IntVar()
slider = tk.Scale(input_frame, variable=boardsize,
                  from_=3, to=9,
                  orient=tk.HORIZONTAL)
slider.pack()

# remove fixed size so frame will shrink to sheet
board_frame = tk.Frame(root)
board_frame.pack(expand=True, fill="both")

sheet = tksheet.Sheet(board_frame)
sheet.set_options(table_alignment="center")
sheet.grid()

BackendBoard = None

def generateboard():
    size = boardsize.get()
    board_frame.pack(expand=True, fill="both")
    # reuse the same sheet widget instead of recreating it
    sheet.set_sheet_data([])               # clear existing data
    sheet.grid()
    board_frame.rowconfigure(0, weight=1)
    board_frame.columnconfigure(0, weight=1)
    sheet.grid(row=0, column=0, sticky="nsew")
    create_sudoku_sheet()
    solve_board_bt['state'] = tk.NORMAL

def generatesolvedboard(solved_board):
    if solved_board:
        sheet.set_sheet_data(solved_board)
        sheet.set_all_cell_sizes_to_text()
    else:
        print("Board cannot be solved")

make_board = tk.Button(input_frame, text="make the board", command=generateboard)
make_board.pack()

def z3_solve():
    actual_size = boardsize.get() * boardsize.get()
    grid = [[BackendBoard[j, i] for j in range(actual_size)]
            for i in range(actual_size)]
    cnf = sudoku_to_cnf(grid, actual_size)
    solution = z3solver.solve_cnf(cnf)
    return cnf_to_sudoku(solution, actual_size) if solution else None

def generic_sat_solve(solver_module):
    actual_size = boardsize.get() * boardsize.get()
    grid = [[BackendBoard[j, i] for j in range(actual_size)]
            for i in range(actual_size)]
    cnf = sudoku_to_cnf(grid, actual_size)
    solution = solver_module.solve_cnf(cnf)
    return cnf_to_sudoku(solution, actual_size) if solution else None

def solveboard():
    solve_board_bt['state'] = tk.DISABLED
    start = time.time()

    if selected_solver.get() == "Z3":
        solved_board = z3_solve()
    else:  # PySAT
        print("Solving board with PySAT...")
        solved_board = generic_sat_solve(pysat_solver)

    end = time.time()
    generatesolvedboard(solved_board)

    elapsed = end - start
    hrs, rem = divmod(elapsed, 3600)
    mins, rem = divmod(rem, 60)
    secs, ms = divmod(rem, 1)
    time_str = f"Solved in {int(hrs)}h {int(mins)}m {int(secs)}s {int(ms*1000)}ms"
    # place time under board
    if hasattr(root, 'time_label'):
        root.time_label.config(text=time_str)
    else:
        root.time_label = tk.Label(root, text=time_str)
        root.time_label.pack()

select_difficult_menu = tk.OptionMenu(input_frame, selected_difficulty, *difficulty_levels)
select_difficult_menu.pack()

select_solver_menu = tk.OptionMenu(input_frame, selected_solver, *solvers)
select_solver_menu.pack()

solve_board_bt = tk.Button(input_frame, text="Solve the board", state=tk.DISABLED, command=solveboard)
solve_board_bt.pack()

def create_sudoku_sheet():
    global sheet, BackendBoard
    size = boardsize.get()
    actual_size = size * size

    if selected_difficulty.get() == "Easy":
        BackendBoard = Sudoku_Generator.run(size, 0)
    elif selected_difficulty.get() == "Medium":
        BackendBoard = Sudoku_Generator.run(size, 1)
    else:
        BackendBoard = Sudoku_Generator.run(size, 2)

    test_data = [[
        " " if BackendBoard[cj, ri] == 0 else f"{BackendBoard[cj, ri]}"
        for cj in range(actual_size)] for ri in range(actual_size)]
    sheet.set_sheet_data(test_data)
    sheet.set_all_cell_sizes_to_text()

    try:
        sheet.enable_bindings(("arrowkeys", "right", "left", "up", "down"))
    except Exception as e:
        print(f"error adding bindings to sheet: {e}")

def reset_board():
    for child in board_frame.winfo_children():
        child.destroy()

root.mainloop()
