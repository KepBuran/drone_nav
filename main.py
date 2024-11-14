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
import matplotlib.pyplot as plt

DRAW_ENVIRONMENT = True

IS_GREEDY = False
IS_AREAS = True
IS_CLUSTER = False   

IS_DRAW_AREAS = True

SCREEN_WIDTH = 1000 # 1500
SCREEN_HEIGHT = 900
CELL_SIZE = 50 # 5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

SPEED = 5
GROWTH_RATE = 0.005 * 5

grid_generator = GridGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
grid = grid_generator.generate_grid(CELL_SIZE)
grid_drawer = GridDrawer(pygame, screen, draw_grid_lines=DRAW_ENVIRONMENT)

swarm = Swarm(pygame, screen, grid, SPEED, init_drones_amount=4, is_draw=DRAW_ENVIRONMENT)

logger = Logger(pygame, screen, grid, is_log_on_screen=DRAW_ENVIRONMENT)

greedy = Greedy(grid, swarm.drones)
cluster_algorithm = Cluster(grid, swarm.drones)
areas_algorithm = Areas(grid, swarm.drones)

if (IS_AREAS):
    swarm.set_algorithm(areas_algorithm)

if (IS_CLUSTER):
    cluster_algorithm.calculate_cluster()
    swarm.set_algorithm(cluster_algorithm)


iterations = 0


while True:
    iterations += 1

    if (iterations % 2000 == 0 and iterations != 0):
        grid = grid_generator.generate_grid(CELL_SIZE)
        swarm.set_grid(grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Screen background color
    screen.fill((0, 0, 0))

    if (IS_AREAS and IS_DRAW_AREAS and DRAW_ENVIRONMENT):
        grid_drawer.draw_clusters(grid, areas_algorithm.areas_grid, len(swarm.drones))

    if (IS_CLUSTER and IS_DRAW_AREAS and DRAW_ENVIRONMENT):
        grid_drawer.draw_clusters(grid, cluster_algorithm.clusters_grid, len(swarm.drones))

    # Grid logic 
    if (DRAW_ENVIRONMENT):
        grid_drawer.draw(grid)
        
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


cells_sum_list = logger.cells_sum_list

# Draw the graph

print('Plotting the graph...')
plt.plot(cells_sum_list)
plt.xlabel('Time Step')
plt.ylabel('Cells Sum')
plt.title('Cells Sum Over Time')
plt.grid(True)
plt.show()