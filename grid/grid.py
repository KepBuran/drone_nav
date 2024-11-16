import math
import copy

class Grid:
    def __init__(self, cell_size, grid_width, grid_height, x_offset=0, y_offset=0, draw_grid_lines=False):
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.draw_grid_lines = draw_grid_lines
        self.grid = [[1 for _ in range(math.floor(grid_width // cell_size))] for _ in range(math.floor(grid_height // cell_size))]
        self.growth_grid = copy.deepcopy(self.grid)

    def increase(self, growth_rate=0.1):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                # self.grid[row][col] += 1 * growth_rate
                self.grid[row][col] += self.growth_grid[row][col] * growth_rate
                # if (self.growth_grid[row][col] > 1):
                    # print("Growth grid value: ", self.growth_grid[row][col])

    def get_cells_sum(self):
        return sum(sum(row) for row in self.grid)
    
    def get_cells_amount(self):
        return len(self.grid) * len(self.grid[0])
    
    def get_growth_sum(self):
        return sum(sum(row) for row in self.growth_grid)
    
    def get_cell_by_coords(self, x, y):
        row = (y - self.y_offset) // self.cell_size
        col = (x - self.x_offset) // self.cell_size
        return [int(row), int(col)]
    
    def nearest_cells_by_coords(self, x, y, n):
        row, col = self.get_cell_by_coords(x, y)
        # return cells with values in a nxn grid around the given cell 
        return [(self.grid[i][j], i, j) 
                for i in range(max(0, row - n), min(len(self.grid), row + n + 1)) 
                for j in range(max(0, col - n), min(len(self.grid[0]), col + n + 1))]

    def cell_center_coords(self, row, col):
        return (col * self.cell_size + self.cell_size // 2 + self.x_offset, row * self.cell_size + self.cell_size // 2 + self.y_offset)

    def set_cell_value(self, row, col, value):
        self.grid[row][col] = value

    def set_cell_value_in_radius(self, row, col, value, radius):
        if (radius == 0):
            if (row >= 0 and row < len(self.grid) and col >= 0 and col < len(self.grid[0])):
                self.grid[row][col] = value
            else:
                # print("set_cell_value_in_radius Out of bounds", row, col)
                pass
            return


        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                new_row = row + i
                new_col = col + j
                if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                    self.grid[new_row][new_col] = value

    