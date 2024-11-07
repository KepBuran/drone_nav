import numpy as np
from sklearn.cluster import KMeans

class Areas:
    def __init__(self, grid, drones):
        self.grid = grid
        self.drones = drones
        self.areas_grid = self.grid.growth_grid.copy()
    

    def make_areas(self): 
        areas_amount = len(self.drones)
        growth_sum = self.grid.get_growth_sum()
        growth_per_area = growth_sum / areas_amount

        areas_grid = []

        current_area = 0
        growth_current_sum = 0
        for row in range(len(self.grid.growth_grid)):
            areas_grid.append([])
            for col in range(len(self.grid.growth_grid[0])):
                growth_current_sum += self.grid.growth_grid[row][col]
                if (growth_per_area * (current_area + 1) >= growth_current_sum):
                    areas_grid[row].append(current_area)
                    continue
                current_area += 1
                areas_grid[row].append(current_area)
        
        self.areas_grid = areas_grid

                    


  



