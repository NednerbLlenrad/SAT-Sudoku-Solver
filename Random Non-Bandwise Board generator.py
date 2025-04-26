import random
import time

class SudokuBoard:
    def __init__(self, block_size):
        self.block_size = block_size
        self.size = block_size ** 2
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def is_safe(self, row, col, num):
        block_row = row - row % self.block_size
        block_col = col - col % self.block_size
        for i in range(self.size):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        for i in range(self.block_size):
            for j in range(self.block_size):
                if self.grid[block_row + i][block_col + j] == num:
                    return False
        return True

    def fill_diagonal_boxes(self):
        for k in range(0, self.size, self.block_size):
            nums = list(range(1, self.size + 1))
            random.shuffle(nums)
            for i in range(self.block_size):
                for j in range(self.block_size):
                    self.grid[k + i][k + j] = nums.pop()

    def fill_boxwise_random(self):
        for box_row in range(0, self.size, self.block_size):
            for box_col in range(0, self.size, self.block_size):
                if box_row == box_col:
                    continue  # Skip already-filled diagonal boxes

                nums = list(range(1, self.size + 1))
                random.shuffle(nums)
                for i in range(self.block_size):
                    for j in range(self.block_size):
                        row = box_row + i
                        col = box_col + j
                        placed = False
                        random.shuffle(nums)
                        for num in nums:
                            if self.is_safe(row, col, num):
                                self.grid[row][col] = num
                                placed = True
                                break
                        if not placed:
                            self.grid[row][col] = 0  # Leave blank if no valid number found

    def generate(self):
        print("Using non-solver random fill...")
        self.fill_diagonal_boxes()
        self.fill_boxwise_random()

    def dig_holes(self, removal_count):
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        for _ in range(removal_count):
            if not cells:
                break
            r, c = cells.pop()
            self.grid[r][c] = 0

    def display(self):
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

if __name__ == "__main__":
    block_size = int(input("Enter block size (e.g., 3 for 9x9, 5 for 25x25): "))
    board = SudokuBoard(block_size)

    start = time.time()
    board.generate()
    print(f"Generated random board in {time.time() - start:.2f} seconds")

    removal_ratio = 0.5
    removal_count = int(board.size * board.size * removal_ratio)
    board.dig_holes(removal_count)

    board.display()
