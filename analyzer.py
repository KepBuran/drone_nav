import json
import matplotlib.pyplot as plt
import math

cluster = [
    'results/Cluster/dronesAmount=2;cellSize=5;2024-11-17 10:32:21',
    'results/Cluster/dronesAmount=4;cellSize=5;2024-11-17 12:01:33',
    'results/Cluster/dronesAmount=8;cellSize=5;2024-11-17 13:50:25'
]

equal_areas = [
    'results/EqualAreas/dronesAmount=2;cellSize=5;2024-11-17 06:04:50',
    'results/EqualAreas/dronesAmount=4;cellSize=5;2024-11-17 07:36:17',
    'results/EqualAreas/dronesAmount=8;cellSize=5;2024-11-17 09:05:48'
]

equal_interest = [
    'results/EqualInterest/dronesAmount=2;cellSize=5;2024-11-17 01:37:53',
    'results/EqualInterest/dronesAmount=4;cellSize=5;2024-11-17 03:05:10',
    'results/EqualInterest/dronesAmount=8;cellSize=5;2024-11-17 04:35:17',
    'results/EqualInterest/dronesAmount=8;cellSize=10;2024-11-17 15:08:32',
    'results/EqualInterest/dronesAmount=2;cellSize=10;2024-11-17 15:22:36'
]

def read_all_data(folder):
    grids_data_file = f'./{folder}/grids_data.json'
    interest_file = f'./{folder}/interest.json'
    meta_data_file = f'./{folder}/meta_data.json'

    # Parse the interest file
    with open(interest_file, 'r') as file:
        interest = json.load(file)

    # Parse the grids data file
    with open(grids_data_file, 'r') as file:
        grids_data = json.load(file)

    # Parse the meta data file
    with open(meta_data_file, 'r') as file:
        meta_data = json.load(file)

    return interest, grids_data, meta_data

def get_analysis_data(interest, grids_data):
    interest[0].append(interest[0][-1])
    average_interest_list = []

    for i in range(len(interest[0])):
        total = 0
        for j in range(len(interest)):
            if isinstance(interest[j][i], (int, float)):  # Check if the type is int or float
                total += interest[j][i]
        average_interest_list.append(total / len(interest))

    average_interest = sum(average_interest_list) / len(average_interest_list)
    analysis_data = {
        'average_interest': average_interest
    }

    return analysis_data, average_interest_list

def get_grids_average_data(grids_data):
    growth_sums = [grid['growth_sum'] for grid in grids_data]
    average_growth_sum = sum(growth_sums) / len(growth_sums)
    grids_average_data = {
        'average_growth_sum': average_growth_sum
    }

    return grids_average_data

current_folder = equal_interest[4]
print('Current folder:', current_folder)

interest, grids_data, meta_data = read_all_data(current_folder)

analysis_data, average_interest_list = get_analysis_data(interest, grids_data)
grids_average_data = get_grids_average_data(grids_data)

print('Analysis Data:', analysis_data)
print('Grids Average Data:', grids_average_data)

print('Plotting the graph...')
plt.plot(interest[1])
plt.xlabel('Time Step')
plt.ylabel('Cells Sum')
plt.title('Average Cells Sum Over Time')
plt.grid(True)
plt.show()

# Save plots to a file
print('Saving the plot to a file...')
plot_file = './' + current_folder + '/plot.png'
plt.savefig(plot_file)
