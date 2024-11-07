from drone.drone import Drone

class Swarm:
    def __init__ (self, pygame, screen, grid, speed, radius=2):
        self.drones = []
        self.pygame = pygame
        self.grid = grid
        self.screen = screen
        self.speed = speed
        self.radius = radius

        self.init_drones(4)
        
    def init_drones(self, drones_amount):
        # TODO: Implement the logic to create drones without hardcoded positions
        # Hardcoded array for positions
        positions = [(300, 200), (400, 200), (500, 200), (600, 200)]

        # Loop to create drones based on positions
        for position in positions:
            self.drones.append(Drone(self.pygame, self.screen, position, self.speed, (1, 1)))

    def update(self):
        for drone in self.drones:
            # Update and draw each drone
            drone.update()
            # drone.draw()

            # Get the cell by the drone's coordinates
            # cell = self.grid.get_cell_by_coords(drone.position.x, drone.position.y)
            
            # Set the cell value in the radius for each drone
            # self.grid.set_cell_value_in_radius(cell[0], cell[1], 0, drone.radius)
        
        