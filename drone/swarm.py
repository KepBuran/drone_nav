from drone.drone import Drone

class Swarm:
    def __init__ (self, pygame, screen, grid, speed, radius=2, init_drones_amount=4, is_draw=True):
        self.drones = []
        self.pygame = pygame
        self.grid = grid
        self.screen = screen
        self.speed = speed
        self.radius = radius
        self.algorithm = None

        self.is_draw = is_draw
        self.is_env_changed = False

        self.init_drones(init_drones_amount)

    def set_grid(self, grid):
        self.grid = grid
        self.algorithm.grid = grid
        self.is_env_changed = True

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        
    def init_drones(self, drones_amount):
        # TODO: Implement the logic to create drones without hardcoded positions
        # Hardcoded array for positions
        positions = [(300, 200), (400, 250), (500, 300), (600, 400)]

        # Loop to create drones based on positions
        for position in positions:
            self.drones.append(Drone(self.pygame, self.screen, position, self.speed, (1, 1)))

    def update(self):
        self.algorithm.run(self.is_env_changed)
        self.is_env_changed = False

        for drone in self.drones:
            # Update and draw each drone
            drone.update()
            if (self.is_draw):
                drone.draw()

            # Get the cell by the drone's coordinates
            cell = self.grid.get_cell_by_coords(drone.position.x, drone.position.y)
            
            # Set the cell value in the radius for each drone
            self.grid.set_cell_value_in_radius(cell[0], cell[1], 0, drone.radius)
        
        