import pygame
from sys import exit
from areas.areas import Areas
from cluster.cluster import Cluster
from greedy import Greedy
from grid.drawer import GridDrawer
from grid.generator import GridGenerator
from grid.grid import Grid
from drone.drone import Drone
import random
from logger import Logger

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
CELL_SIZE = 4

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

speed = 5
growth_rate = 0.005 * 5

grid_generator = GridGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)

grid = grid_generator.generate_grid(CELL_SIZE)
grid_drawer = GridDrawer(pygame, screen)

logger = Logger(pygame, screen, grid)

iterations = 0

drones = []

# Create multiple drones with different positions and directions
drones.append(Drone(pygame, screen, (300, 200), speed, (1, 1)))
drones.append(Drone(pygame, screen, (300, 200), speed, (1, 1)))
drones.append(Drone(pygame, screen, (300, 200), speed, (1, 1)))
drones.append(Drone(pygame, screen, (300, 200), speed, (1, 1)))

areas_algorithm = Areas(grid, drones)

areas_algorithm.make_areas()
grid_drawer.draw_clusters(grid, areas_algorithm.areas_grid, len(drones))
grid.increase(30)
grid_drawer.draw(grid) 

while True:
    iterations += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Screen background color
    # screen.fill((0, 0, 0))

    # Grid logic 
    # grid.increase(growth_rate)
    # grid_drawer.draw(grid) 

    # Logger logic
    # logger.log_grid_sum()
    # logger.log_iteration(iterations)

    pygame.display.update()
    clock.tick(100)
    