#Sudoku Rules: No 2 of the same number in any, nxn grid, any row, any collum
#bandwise fill, DFS too slow
import random

class SudokuBoard:
    def __init__(self, block_size):
        # Creates an empty grid of size block_size^2 x block_size^2
        self.block_size = block_size
        self.size = block_size ** 2
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def is_safe(self, row, col, num):
        # Check if a number can be safely placed in grid[row][col]
        # Ensures no conflicts in row, column, or box
        for i in range(self.size):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        start_row = row - row % self.block_size
        start_col = col - col % self.block_size
        for i in range(self.block_size):
            for j in range(self.block_size):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def fill_diagonal_boxes(self):
        # Pre-fills the diagonal boxes as they do not overlap
        for k in range(0, self.size, self.block_size):
            nums = list(range(1, self.size + 1))
            random.shuffle(nums)
            for i in range(self.block_size):
                for j in range(self.block_size):
                    self.grid[k + i][k + j] = nums.pop()

    def fill_remaining_bands(self):
        # Band-wise fill: Fill rows and columns by shuffling within bands/stacks
        # Fill rows in bands
        for band in range(0, self.size, self.block_size):
            ribs = [r for r in range(band, band + self.block_size)]
            random.shuffle(ribs)
            for i, r in enumerate(ribs):
                if r != band + i:
                    self.grid[r], self.grid[band + i] = self.grid[band + i], self.grid[r]

        # Fill columns in stacks
        for stack in range(0, self.size, self.block_size):
            cis = [c for c in range(stack, stack + self.block_size)]
            random.shuffle(cis)
            for i, c in enumerate(cis):
                if c != stack + i:
                    for row in self.grid:
                        row[c], row[stack + i] = row[stack + i], row[c]

    def dig_holes(self, removal):
        # Randomly removes cells from the filled board to create a puzzle
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        for _ in range(removal):
            if not cells:
                break
            r, c = cells.pop()
            self.grid[r][c] = 0

    def display(self):
        # Prints the Sudoku board to the console with separators for boxes
        sep = "-" * (self.size * 2 + self.block_size + 1)
        for i in range(self.size):
            if i % self.block_size == 0:
                print(sep)
            for j in range(self.size):
                if j % self.block_size == 0:
                    print("|", end=" ")
                val = self.grid[i][j]
                print(f"{val if val != 0 else '.'}", end=" ")
            print("|")
        print(sep)
        
    def valueReturn(self, x:int, y:int):
        return self.grid[x][y]



if __name__ == "__main__":
    block_size = int(input("Enter block size (e.g., 3 for 9x9, 5 for 25x25): "))
    board = SudokuBoard(block_size)

    board.fill_diagonal_boxes()
    board.fill_remaining_bands()

    removal_ratio = 0.5  # Adjust this value to control puzzle difficulty
    removal_count = int(board.size * board.size * removal_ratio)
    board.dig_holes(removal_count)

    board.display()

def run(block_size):
    board = SudokuBoard(block_size)

    board.fill_diagonal_boxes()
    board.fill_remaining_bands()

    removal_ratio = 0.5  # Adjust this value to control puzzle difficulty
    removal_count = int(board.size * board.size * removal_ratio)
    board.dig_holes(removal_count)
    return board
    #board.display()
