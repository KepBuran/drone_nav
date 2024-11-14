import numpy as np
from sklearn.cluster import KMeans
from hungarian_algorithm import HungarianAlgorithm

class Areas:
    def __init__(self, grid, drones):
        self.grid = grid
        self.drones = drones
        self.areas_grid = self.grid.growth_grid.copy()
        self.areas = []
        self.drone_pathes = []
        self.drone_aims = []
    

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
                if (current_area == areas_amount - 1):
                    areas_grid[row].append(current_area)
                    continue
                current_area += 1
                areas_grid[row].append(current_area)
        
        self.areas_grid = areas_grid

        # Initialize areas array and then populate it with cells coords and indexes for each area
        self.areas = [[] for _ in range(areas_amount)]

        for i in range(areas_amount):
            for row in range(len(self.areas_grid)):
                maybe_row = []
                for col in range(len(self.areas_grid[row])):
                    if (self.areas_grid[row][col] == i):
                        maybe_row.append([(row, col), self.grid.cell_center_coords(row, col)])
                if (len(maybe_row) > 0):
                    self.areas[i].append(maybe_row)

    def calculate_distance(self, drone, area, area_index):
        #Check if drone is already in the area
        drone_cell = self.grid.get_cell_by_coords(drone.position.x, drone.position.y)

        if (self.areas_grid[drone_cell[0]][drone_cell[1]] == area_index):
            return 0

        # Find nearest area cell to the drone
        drone_x, drone_y = drone.position.x, drone.position.y

        min_distance = float('inf')
        for row in area:
            for cell in row:
                if cell is not None:
                    cell_x, cell_y = cell[1]
                    distance = np.sqrt((drone_x - cell_x)**2 + (drone_y - cell_y)**2)
                    if distance < min_distance:
                        min_distance = distance
        
        return min_distance

    def set_drones_to_areas(self):

        # Calculate min distance from each drone to each area
        distances = np.zeros((len(self.drones), len(self.areas)))
        for i, drone in enumerate(self.drones):
            for j, area in enumerate(self.areas):
                distances[i][j] = self.calculate_distance(drone, area, j)

        # print("Drones to areas distances:\n", distances)
        result = HungarianAlgorithm(distances).solve()
        # print("Result of hungarian algorithm:\n", result)

        self.drones_to_areas = result

    def find_area_cell(self, area, row_index, col_index):
        area_row_offset = area[0][0][0][0]

        area_row_index = row_index - area_row_offset

        if (area_row_index < 0 or area_row_index >= len(area)):
            return None
        
        for cell in area[area_row_index]:
            if cell is not None and cell[0][1] == col_index:
                return cell
            
        return None

    def build_drone_path(self, drone, area):
        # Path is circular, so drone will visit all cells in the area and return to the starting point
        # For it start from the first cell of row, where first cell x index is 0
        # Then go to the last cell of the column
        # Then go to the last cell of next column
        # Then go to the second cell of the column
        # Repeat it until the last cell of the row is reached
        # Then go to the first cell of the column and go to the initial cell going throw all first cells in the column

        # Build list of the path

        path = []
        row_min_index = min(cell[0][0] for row in area for cell in row)
        col_min_index = min(cell[0][1] for row in area for cell in row)
        
        row_max_len = len(area)
        col_max_len = max(len(row) for row in area)

        initial_cell = area[0][0]
        # print("Initial cell", initial_cell)
        if (initial_cell[0][1] != 0):
            initial_cell = area[1][0]

        col_index = initial_cell[0][1]
        row_index = initial_cell[0][0]
        
        cell = initial_cell
        path.append(cell)

        while True:
            # print("Current path", [cell[0] for cell in path])
            if (not cell[0][1] % 2):
                maybe_cell = self.find_area_cell(area, cell[0][0] + 1, cell[0][1])
                if maybe_cell is not None:
                    cell = maybe_cell
                    path.append(cell)
                    continue

                if (cell[0][1] == col_max_len - 1):
                    break

                maybe_cell = self.find_area_cell(area, cell[0][0] + 1, cell[0][1] + 1)
                if maybe_cell is None:
                    maybe_cell = self.find_area_cell(area, cell[0][0], cell[0][1] + 1)
                if maybe_cell is None:
                    maybe_cell = self.find_area_cell(area, cell[0][0] - 1, cell[0][1] + 1)
                
                cell = maybe_cell
                path.append(cell)

            else:
                cell = self.find_area_cell(area, cell[0][0] - 1, cell[0][1])
                path.append(cell)
                # Ячейка після наступної
                maybe_next_next_cell = self.find_area_cell(area, cell[0][0] - 2, cell[0][1])
                if maybe_next_next_cell is None:
                    if (cell[0][1] == col_max_len - 1):
                        break
                    maybe_cell = self.find_area_cell(area, cell[0][0] - 2, cell[0][1] + 1)
                    if (maybe_cell):
                        cell = self.find_area_cell(area, cell[0][0] - 1, cell[0][1] + 1)
                        path.append(cell)
                        continue

                    maybe_cell = self.find_area_cell(area, cell[0][0] - 1, cell[0][1] + 1)
                    if (maybe_cell):
                        cell = self.find_area_cell(area, cell[0][0], cell[0][1] + 1)
                        path.append(cell)
                        continue

                    cell = self.find_area_cell(area, cell[0][0] + 1, cell[0][1] + 1)   
                    path.append(cell) 

        if (cell[0][1] % 2 == 0):
            print("Cell", cell, "is odd")
            while True: 
                maybe_cell = self.find_area_cell(area, cell[0][0], cell[0][1] - 1)
                if (maybe_cell is None):
                    break
                cell = maybe_cell
                path.append(cell)

        while True:
            print("Cell", cell, initial_cell)
            if (cell[0][0] == initial_cell[0][0] and cell[0][1] == initial_cell[0][1]):
                break

            maybe_cell = self.find_area_cell(area, cell[0][0] - 1, cell[0][1] - 1)
            if (maybe_cell):
                cell = maybe_cell
                path.append(cell)
                continue
            maybe_cell = self.find_area_cell(area, cell[0][0], cell[0][1] - 1)
            if (maybe_cell):
                cell = maybe_cell
                path.append(cell)
                continue
    
            cell = self.find_area_cell(area, cell[0][0] + 1, cell[0][1] - 1)   
            path.append(cell) 

        path.pop()

        # print("Path for drone", "is", [cell[0] for cell in path])
        return path 

    def build_drone_paths(self):
        self.drone_pathes = []
        # Build path for each drone
        for i, drone in enumerate(self.drones):
            area_index = self.drones_to_areas[i][1]
            area = self.areas[area_index]
            self.drone_pathes.append(self.build_drone_path(drone, area))
            # drone.set_path(path)
        
        # print("Drone pathes", self.drone_pathes)

    def set_initial_drones_aims(self):
        self.drone_aims = []
        for i, drone in enumerate(self.drones):
            path = self.drone_pathes[i]
            # Find closest cell to the drone in the path
            min_distance = float('inf')
            min_distance_index = -1
            for j, cell in enumerate(path):
                cell_x, cell_y = cell[1]
                drone_x, drone_y = drone.position.x, drone.position.y
                distance = np.sqrt((drone_x - cell_x)**2 + (drone_y - cell_y)**2)
                if distance < min_distance:
                    min_distance = distance
                    min_distance_index = j
            
            self.drone_aims.append([path[min_distance_index], min_distance_index])
            drone.set_direction_by_coords(path[min_distance_index][1])

        # print("Initial drones aims", self.drone_aims)
    
    def set_next_drones_aim(self):
        for index in range(len(self.drones)):
            drone = self.drones[index]
            aim = self.drone_aims[index]
            drone_cell = self.grid.get_cell_by_coords(drone.position.x, drone.position.y)

            if (drone_cell[0] < 0 or drone_cell[1] < 0):
                print("Drone is out of the grid", "drone index", index, "drone cell", drone_cell, "drone aim", aim)

            if (drone_cell[0] == aim[0][0][0] and drone_cell[1] == aim[0][0][1]):
                path = self.drone_pathes[index]
                aim_index = aim[1]
             
                if (aim_index == len(path) - 1):
                    aim_index = 0
                else:
                    aim_index += 1
                self.drone_aims[index] = [path[aim_index], aim_index]
                drone.set_direction_by_coords(path[aim_index][1])

    def run(self):

        if (not self.grid.is_changed):
            self.set_next_drones_aim()
            return
        print("Running areas algorithm")

        print('Grid length', len(self.grid.grid[0]))

        self.make_areas()
        self.set_drones_to_areas()
        self.build_drone_paths()
        self.set_initial_drones_aims()

        self.grid.is_changed = False

    
                    


  



