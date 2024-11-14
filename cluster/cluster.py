import numpy as np
from sklearn.cluster import KMeans
from hungarian_algorithm import HungarianAlgorithm
from stc.STC import STC
import math

class Cluster:
    def __init__(self, grid, drones):
        self.grid = grid
        self.drones = drones
        self.clusters_grid = [[]]
        self.drones_to_clusters = []

    def get_points(self):
        points = []
        for i in range(len(self.grid.growth_grid)):
            for j in range(len(self.grid.growth_grid[0])):
                m = self.grid.growth_grid[i][j]
                for _ in range(m):
                    points.append([i, j])
        # Use points as needed, for example, pass to kmeans_equal
        return points
    
    def get_clusters_grid(self, points, labels):
        grid = []
        for i in range(len(self.grid.growth_grid)):
            grid.append([0] * len(self.grid.growth_grid[0]))
        for i in range(len(points)):
            point = points[i]
            grid[point[0]][point[1]] = labels[i]
        return grid

    def calculate_distance(self, drone, cluster, cluster_index):
        #Check if drone is already in the cluster
        drone_cell = self.grid.get_cell_by_coords(drone.position.x, drone.position.y)

        if (self.clusters_grid[drone_cell[0]][drone_cell[1]] == cluster_index):
            return 0

        # Find nearest cluster cell to the drone
        drone_x, drone_y = drone.position.x, drone.position.y

        min_distance = float('inf')
        for row in cluster:
            for cell in row:
                if cell is not None:
                    cell_x, cell_y = cell[1]
                    distance = np.sqrt((drone_x - cell_x)**2 + (drone_y - cell_y)**2)
                    if distance < min_distance:
                        min_distance = distance
        
        return min_distance

    def set_drones_to_clusters(self):
        # Calculate min distance from each drone to each cluster
        distances = np.zeros((len(self.drones), len(self.clusters)))
        for i, drone in enumerate(self.drones):
            for j, cluster in enumerate(self.clusters):
                distances[i][j] = self.calculate_distance(drone, cluster, j)

        # print("Drones to clusters distances:\n", distances)
        result = HungarianAlgorithm(distances).solve()
        # print("Result of hungarian algorithm:\n", result)

        self.drones_to_clusters = result
        print("Drones to clusters:\n", self.drones_to_clusters)

    def calculate_cluster(self):
        n = len(self.drones)
        points = self.get_points()
        cluster_size = len(points) // n

        kmeans = KMeans(n_clusters=n, random_state=0).fit(points)
        
        self.clusters_grid = self.get_clusters_grid(points, kmeans.labels_)
        
        self.clusters = [[] for _ in range(n)]

        for i in range(n):
            for row in range(len(self.clusters_grid)):
                maybe_row = []
                for col in range(len(self.clusters_grid[row])):
                    if (self.clusters_grid[row][col] == i):
                        maybe_row.append([(row, col), self.grid.cell_center_coords(row, col)])
                if (len(maybe_row) > 0):
                    self.clusters[i].append(maybe_row)

    def find_cluser_cell(self, cluster, row_index, col_index):
        cluster_row_offset = cluster[0][0][0][0]

        cluster_row_index = row_index - cluster_row_offset

        if (cluster_row_index < 0 or cluster_row_index >= len(cluster)):
            return None
        
        for cell in cluster[cluster_row_index]:
            if cell is not None and cell[0][1] == col_index:
                return cell
            
        return None

    def get_stc_cluster_grid(self, cluster):
        # print('CLUSTER', [cell[0] for row in cluster for cell in row])  

        max_col_len = max([len(col) for col in cluster])
        max_row_len = len(cluster)

        min_row_index = min([row[0][0][0] for row in cluster])
        min_col_index = min([cell[0][1] for row in cluster for cell in row if cell is not None])

        # print("Cluster min row index", min_row_index, "Cluster min col index", min_col_index, "Cluster max row len", max_row_len, "Cluster max col len", max_col_len)

        col_max = round((max_col_len + 0.1) / 2)
        row_max = round((max_row_len + 0.1) / 2)
        # print("Col max", col_max, "Row max", row_max)
        grid = [[None for _ in range(col_max)] for _ in range(row_max)]

        start_point = None

        for row in range(row_max):  
            for col in range(col_max):
                cells = [
                    self.find_cluser_cell(cluster, row * 2 + min_row_index, col * 2 + min_col_index),
                    self.find_cluser_cell(cluster, row * 2 + 1 + min_row_index, col * 2 + min_col_index),
                    self.find_cluser_cell(cluster, row * 2 + min_row_index, col * 2 + min_col_index + 1),
                    self.find_cluser_cell(cluster, row  * 2 + 1 + min_row_index, col * 2 + min_col_index + 1)
                ]
                # print("row", row, "col", col)
                if all(cell is None for cell in cells):
                    grid[row][col] = 1
                else:
                    grid[row][col] = 0
                    if start_point is None:
                        start_point = (row, col)

        return grid, start_point

    def stc_path_to_cluster(self, cluster, stc_path):
        min_row_index = min([row[0][0][0] for row in cluster])
        min_col_index = min([cell[0][1] for row in cluster for cell in row if cell is not None])

        path = []

        for cell in stc_path:
            x_index = cell[0] + min_row_index
            y_index = cell[1] + min_col_index
            path.append(((x_index, y_index), self.grid.cell_center_coords(x_index, y_index)))

        # print("Stc path to cluster", [cell[0] for cell in path])
        return path
    
    def clean_up_path(self, path, cluster):
        cleaned_path = []
        for i in range(len(path)):
            cell = path[i]
            cluster_cell = self.find_cluser_cell(cluster, cell[0][0], cell[0][1])
            if cluster_cell is not None:
                cleaned_path.append(cluster_cell)
        return cleaned_path


    def build_drone_path(self, cluster):
        stc_cluster_grid, start_point = self.get_stc_cluster_grid(cluster)
        # print("Stc cluster grid", stc_cluster_grid)

        
        stc = STC()
        stc_path = stc.plan_path(stc_cluster_grid, start_point)
        # print("stc_path", stc_path)
        path = self.stc_path_to_cluster(cluster, stc_path)
        cleaned_path = self.clean_up_path(path, cluster)
        return cleaned_path

    def build_drone_paths(self):
        self.drone_pathes = []
        # Build path for each drone
        for i, drone in enumerate(self.drones):
            cluster_index = self.drones_to_clusters[i][1]
            cluster = self.clusters[cluster_index]
            self.drone_pathes.append(self.build_drone_path(cluster))
            # drone.set_path(path)
        
    def set_initial_drones_aims(self):
        self.drone_aims = []
        for i, drone in enumerate(self.drones):
            path = self.drone_pathes[i]
            # Find closest cell to the drone in the path
            min_distance = float('inf')
            min_distance_index = -1
            for j, cell in enumerate(path):
                # print("Cell", cell)
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
                pass
                # print("Drone is out of the grid", "drone index", index, "drone cell", drone_cell, "drone aim", aim)

            if (drone_cell[0] == aim[0][0][0] and drone_cell[1] == aim[0][0][1]):
                path = self.drone_pathes[index]
                aim_index = aim[1]
             
                if (aim_index == len(path) - 1):
                    aim_index = 0
                else:
                    aim_index += 1
                self.drone_aims[index] = [path[aim_index], aim_index]
                drone.set_direction_by_coords(path[aim_index][1])
            
            else:
                drone.set_direction_by_coords(aim[0][1])

    def run(self, is_env_changed):

        if (not is_env_changed):
            self.set_next_drones_aim()
            return
        print("Running cluster algorithm")

        # print('Grid length', len(self.grid.grid[0]))

        self.calculate_cluster()
        self.set_drones_to_clusters()
        self.build_drone_paths()
        self.set_initial_drones_aims()



