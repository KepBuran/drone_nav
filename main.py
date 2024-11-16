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
from SeededRandom import SeededRandom
import datetime
import os

IS_RENDER = False

IS_GREEDY = False
IS_AREAS = True
IS_CLUSTER = False   

DISTRIBUTION_TYPE = 'equal_interest' # 'equal_interest' or 'equal_areas' 

IS_DRAW_AREAS = False

SCREEN_WIDTH = 1500 # 1500
SCREEN_HEIGHT = 900
CELL_SIZE = 5 # 5

SPEED = 5
GROWTH_RATE = 1

INTERVAL_MULTIPLIER = 50
GRID_GENERATION_INTERVAL = 3000 * INTERVAL_MULTIPLIER
DRONE_AMOUNT_CHANGE_INTERVAL = 1000 * INTERVAL_MULTIPLIER
DRONE_PUSH_INTERVAL = 2000 * INTERVAL_MULTIPLIER

INIT_DRONES_AMOUNT = 8

AMOUNT_OF_GRIDS = 10

iterations_amount = AMOUNT_OF_GRIDS * GRID_GENERATION_INTERVAL

meta_data = {
    'IS_RENDER': IS_RENDER,
    'IS_GREEDY': IS_GREEDY,
    'IS_AREAS': IS_AREAS,
    'IS_CLUSTER': IS_CLUSTER,
    'DISTRIBUTION_TYPE': DISTRIBUTION_TYPE,
    'IS_DRAW_AREAS': IS_DRAW_AREAS,
    'SCREEN_WIDTH': SCREEN_WIDTH,
    'SCREEN_HEIGHT': SCREEN_HEIGHT,
    'CELL_SIZE': CELL_SIZE,
    'SPEED': SPEED,
    'GROWTH_RATE': GROWTH_RATE,
    'INTERVAL_MULTIPLIER': INTERVAL_MULTIPLIER,
    'GRID_GENERATION_INTERVAL': GRID_GENERATION_INTERVAL,
    'DRONE_AMOUNT_CHANGE_INTERVAL': DRONE_AMOUNT_CHANGE_INTERVAL,
    'DRONE_PUSH_INTERVAL': DRONE_PUSH_INTERVAL,
    'INIT_DRONES_AMOUNT': INIT_DRONES_AMOUNT,
    'AMOUNT_OF_GRIDS': AMOUNT_OF_GRIDS
}

seed_str = str(SCREEN_WIDTH) + str(SCREEN_HEIGHT) + str(CELL_SIZE) + str(SPEED) + str(int(GROWTH_RATE)) 
seed_str += str(GRID_GENERATION_INTERVAL) + str(DRONE_AMOUNT_CHANGE_INTERVAL) + str(DRONE_PUSH_INTERVAL)
seed = int(seed_str)

SeededRandom.set_initial_seed(seed)

print('Initializing the environment...')

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()


print('Generating the grid...')
grid_generator = GridGenerator(SCREEN_WIDTH, SCREEN_HEIGHT)
grid = grid_generator.generate_grid(CELL_SIZE)
grid_drawer = GridDrawer(pygame, screen, draw_grid_lines=IS_RENDER and True)

print('Initializing the swarm...')
swarm = Swarm(pygame, screen, grid, SPEED, init_drones_amount=INIT_DRONES_AMOUNT, is_draw=IS_RENDER)

print('Initializing the logger...')
logger = Logger(pygame, screen, grid, is_log_on_screen=IS_RENDER)

print('Initializing the algorithms...')
greedy = Greedy(grid, swarm.drones)
cluster_algorithm = Cluster(grid, swarm.drones)
areas_algorithm = Areas(grid, swarm.drones, distribution_type=DISTRIBUTION_TYPE)

if (IS_AREAS):
    swarm.set_algorithm(areas_algorithm)

if (IS_CLUSTER):
    swarm.set_algorithm(cluster_algorithm)


iterations = 0

print('Starting the simulation...')

amount_of_grids = 1

while True:
    iterations += 1

    # if (iterations % 10 == 0):
    #     break

    if (iterations % 1000 == 0):
        print('Progress: {:.2f}%'.format(iterations / iterations_amount * 100))

    if (iterations % GRID_GENERATION_INTERVAL == 0 and iterations != 0):
        if (amount_of_grids == AMOUNT_OF_GRIDS):
            break

        amount_of_grids += 1
        grid = grid_generator.generate_grid(CELL_SIZE)
        swarm.set_grid(grid)
        logger.set_grid(grid)

    if (iterations % DRONE_AMOUNT_CHANGE_INTERVAL == 0 and iterations != 0):
        if (iterations % DRONE_PUSH_INTERVAL == 0):
            swarm.push_drone()
        else:
            swarm.pop_drone()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Screen background color
    screen.fill((0, 0, 0))

    if (IS_AREAS and IS_DRAW_AREAS and IS_RENDER):
        grid_drawer.draw_clusters(grid, areas_algorithm.areas_grid, len(swarm.drones))

    if (IS_CLUSTER and IS_DRAW_AREAS and IS_RENDER):
        grid_drawer.draw_clusters(grid, cluster_algorithm.clusters_grid, len(swarm.drones))

    # Grid logic 
    if (IS_RENDER):
        grid_drawer.draw(grid)
        
    grid.increase(GROWTH_RATE)

    # Update all swarm drones
    swarm.update()

    if (IS_GREEDY):
        greedy.run()
    

    # Logger logic
    logger.log_grid_sum()
    logger.log_iteration(iterations)
    logger.log_is_even(len(grid.grid[0]))

    pygame.display.update()
    clock.tick(1000)


cells_sum_list = logger.cells_sum_list
grids_data = logger.grids_data

AlgorithmName = ''

if (IS_GREEDY):
    AlgorithmName = 'Greedy'
elif (IS_AREAS):
    if (DISTRIBUTION_TYPE == 'equal_interest'):
        AlgorithmName = 'EqualInterest'
    elif (DISTRIBUTION_TYPE == 'equal_areas'):
        AlgorithmName = 'EqualAreas'
elif (IS_CLUSTER):
    AlgorithmName = 'Cluster'

# Save the data to a file

print('Saving the data to a file...')
# Get date and time for file name

now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")

results_dir = './results/' + AlgorithmName + '/'
os.makedirs(results_dir, exist_ok=True)

# Define the file names
file_name1 = os.path.join(results_dir, f'INTEREST_dronesAmount={INIT_DRONES_AMOUNT};cellSize={CELL_SIZE};{date_time}.txt')
file_name2 = os.path.join(results_dir, f'GRIDS_DATA_dronesAmount={INIT_DRONES_AMOUNT};cellSize={CELL_SIZE};{date_time}.txt')
file_name3 = os.path.join(results_dir, f'META_DATA_dronesAmount={INIT_DRONES_AMOUNT};cellSize={CELL_SIZE};{date_time}.txt')

with open(file_name1, 'w') as file:
    for grid_sum_list in cells_sum_list:
        for grid_sum in grid_sum_list:
            file.write(str(grid_sum) + ',')
        file.write('\n')

with open(file_name2, 'w') as file:
    for grid_data in grids_data:
        file.write(str(grid_data) + '\n')

with open(file_name3, 'w') as file:
    for key, value in meta_data.items():
        file.write(f'{key}: {value}\n')

# Draw the graph

flattened_cells_sum_list = [item for sublist in cells_sum_list for item in sublist]

print('Plotting the graph...')
plt.plot(flattened_cells_sum_list)
plt.xlabel('Time Step')
plt.ylabel('Cells Sum')
plt.title('Cells Sum Over Time')
plt.grid(True)
plt.show()