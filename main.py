import pygame
from sys import exit
from drone.swarm import Swarm
from greedy import Greedy
from grid.drawer import GridDrawer
from grid.generator import GridGenerator
from grid.grid import Grid
from drone.drone import Drone
from areas.areas import Areas
from logger import Logger
from cluster.cluster import Cluster

IS_GREEDY = False
IS_CLUSTER = False   
IS_AREAS = False

IS_DRAW_AREAS = False

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
CELL_SIZE = 4

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

SPEED = 5
GROWTH_RATE = 0.005 * 5

grid_generator = GridGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
grid = grid_generator.generate_grid(CELL_SIZE)
grid_drawer = GridDrawer(pygame, screen, draw_grid_lines=False)

swarm = Swarm(pygame, screen, grid, SPEED)

logger = Logger(pygame, screen, grid)

greedy = Greedy(grid, swarm.drones)
cluster_algorithm = Cluster(grid, swarm.drones)
areas_algorithm = Areas(grid, swarm.drones)

if (IS_AREAS):
    areas_algorithm.make_areas()

if (IS_CLUSTER):
    cluster_algorithm.calculate_cluster()


iterations = 0


while True:
    iterations += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    # Screen background color
    screen.fill((0, 0, 0))

    if (IS_AREAS and IS_DRAW_AREAS):
        grid_drawer.draw_clusters(grid, areas_algorithm.areas_grid, len(swarm.drones))

    if (IS_CLUSTER and IS_DRAW_AREAS):
        grid_drawer.draw_clusters(grid, cluster_algorithm.clusters_grid, len(swarm.drones))

    # Grid logic 
    grid_drawer.draw(grid)
    grid_drawer.draw_clusters
    grid.increase(GROWTH_RATE)

    # Update all swarm drones
    swarm.update()

    if (IS_GREEDY):
        greedy.run()
    

    # Logger logic
    logger.log_grid_sum()
    logger.log_iteration(iterations)

    pygame.display.update()
    clock.tick(1000)
    