from drone.drone import Drone
from SeededRandom import SeededRandom

class Swarm:
    def __init__ (self, pygame, screen, grid, speed, radius=2, init_drones_amount=4, is_draw=True):
        self.drones = []
        self.pygame = pygame
        self.grid = grid
        self.screen = screen
        self.speed = speed
        self.radius = radius
        self.algorithm = None

        self.random = SeededRandom()

        self.is_draw = is_draw
        self.is_env_changed = True

        self.init_drones(init_drones_amount)

    def set_grid(self, grid):
        self.grid = grid
        self.algorithm.grid = grid
        self.is_env_changed = True

    def pop_drone(self):
        self.drones.pop()
        self.is_env_changed = True

    def push_drone(self):
        width, height = self.pygame.display.get_surface().get_size()
        drone = Drone(self.pygame, self.screen, (width*self.random.random(), height * self.random.random()), self.speed, (1, 1))
        self.drones.append(drone)
        self.is_env_changed = True

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        
    def init_drones(self, drones_amount):
        for i in range(drones_amount):
            self.push_drone()
           
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
        
        