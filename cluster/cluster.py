import numpy as np
from sklearn.cluster import KMeans

class Cluster:
    def __init__(self, grid, drones):
        self.grid = grid
        self.drones = drones
        self.clusters_grid = [[]]

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

    def calculate_cluster(self):
        n = len(self.drones)
        points = self.get_points()
        cluster_size = len(points) // n

        kmeans = KMeans(n_clusters=n, random_state=0).fit(points)
        
        self.clusters_grid = self.get_clusters_grid(points, kmeans.labels_)



