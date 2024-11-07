import math


class Greedy:
    def __init__(self, grid, drones):
        self.grid = grid
        self.drones = drones

    def run(self):
        # For all drone set nearest cell with heighest value
        prev_drones_cells = []
        for drone in self.drones:
            nearest_cells = self.grid.nearest_cells_by_coords(drone.position.x, drone.position.y, 50)
            nearest_cells = list(filter(lambda x: x[1] >= 0 and x[2] >= 0 and x[1] < len(self.grid.grid) and x[2] < len(self.grid.grid[0]), nearest_cells))
            # divide first value by distance
            evaluated_cells = []
            for cell in nearest_cells:
                evaluated_cells.append([])
                coords =  self.grid.cell_center_coords(cell[1], cell[2])
                distance = math.sqrt((drone.position.x - coords[0])**2 + (drone.position.y - coords[1])**2)
                value = pow(1 + cell[0], 10) / distance
                evaluated_cells[-1].append(value)
                evaluated_cells[-1].append(coords[0])
                evaluated_cells[-1].append(coords[1])
            evaluated_cells.sort(reverse=True)
            if len(evaluated_cells) < 1:
                # TODO: send drone to the nearest cell with heighest value
               return
            best_cell = evaluated_cells[0]
            for cell in evaluated_cells:
                if (cell[1], cell[2]) in prev_drones_cells:
                    continue
                best_cell = cell
                break
            prev_drones_cells.append(best_cell)
            drone.set_direction_by_coords((evaluated_cells[0][1], evaluated_cells[0][2]))
           

