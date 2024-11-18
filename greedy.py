import math


class Greedy:
    def __init__(self, grid, drones):
        self.grid = grid
        self.drones = drones

    def run(self, is_env_changed):
        # For all drone set nearest cell with heighest value
        prev_drones_cells = []
        
        iterator = 0

        for drone in self.drones:
            iterator += 1
            nearest_cells = self.grid.nearest_cells_by_coords(drone.position.x, drone.position.y, 10)
            nearest_cells = list(filter(lambda x: x[1] >= 0 and x[2] >= 0 and x[1] < len(self.grid.grid) and x[2] < len(self.grid.grid[0]), nearest_cells))
            # divide first value by distance
            evaluated_cells = []
            for cell in nearest_cells:
                evaluated_cells.append([])
                # coords =  self.grid.cell_center_coords(cell[1], cell[2])
                # distance = math.sqrt((drone.position.x - coords[0])**2 + (drone.position.y - coords[1])**2)
                value =  cell[0]
                evaluated_cells[-1].append(value)
                evaluated_cells[-1].append(cell[1])
                evaluated_cells[-1].append(cell[2])
            evaluated_cells.sort(reverse=True)
            if len(evaluated_cells) < 1:
                nearest_cell = self.grid.nearest_cell_to_coords(drone.position.x, drone.position.y)
                nearest_cell_coords = self.grid.cell_center_coords(nearest_cell[0], nearest_cell[1])
                drone.set_direction_by_coords(nearest_cell_coords)
                continue
            best_cell = evaluated_cells[0]
            for cell in evaluated_cells:
                if (str(cell[1]) + '_' + str(cell[2])) in prev_drones_cells:
                    # print("Occupied cell")
                    continue
                best_cell = cell
                break
            prev_drones_cells.append(str(best_cell[1]) + '_' + str(best_cell[2]))
            drone.set_direction_by_coords(self.grid.cell_center_coords(best_cell[1], best_cell[2]))
           

