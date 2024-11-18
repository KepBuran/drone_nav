import json
import matplotlib.pyplot as plt
import math
import pandas as pd

# Initialize a global DataFrame
initial_values = [
    {
        'average_interest': 0,
        'average_interest_per_cell': 0,
        'volatility': 0,
        'algorithm': '',
        'drones_amount': 0,
        'folder': ''
    }
]

global_df = pd.DataFrame(initial_values, columns=[
    'average_interest',
    'average_interest_per_cell',
    'volatility',
    'algorithm',
    'drones_amount',
    'folder'
])

cluster = [
    'results/Cluster/dronesAmount=2;cellSize=10;2024-11-17 16:22:38',
    'results/Cluster/dronesAmount=4;cellSize=10;2024-11-17 16:30:47',
    'results/Cluster/dronesAmount=8;cellSize=10;2024-11-17 16:38:49',
    'results/Cluster/dronesAmount=4;cellSize=10;2024-11-17 18:35:25'
]

equal_areas = [
    'results/EqualAreas/dronesAmount=2;cellSize=10;2024-11-17 15:59:48',
    'results/EqualAreas/dronesAmount=4;cellSize=10;2024-11-17 16:07:30',
    'results/EqualAreas/dronesAmount=8;cellSize=10;2024-11-17 16:14:38',
    'results/EqualAreas/dronesAmount=4;cellSize=10;2024-11-17 17:56:55'
]

equal_interest = [
    'results/EqualInterest/dronesAmount=2;cellSize=10;2024-11-17 15:36:01',
    'results/EqualInterest/dronesAmount=4;cellSize=10;2024-11-17 15:44:04',
    'results/EqualInterest/dronesAmount=8;cellSize=10;2024-11-17 15:52:04',
    'results/EqualInterest/dronesAmount=4;cellSize=10;2024-11-17 17:18:01'
]

greedy = [
    'results/Greedy/dronesAmount=2;cellSize=10;2024-11-18 12:02:59',
    'results/Greedy/dronesAmount=4;cellSize=10;2024-11-18 12:11:29',
    'results/Greedy/dronesAmount=4;cellSize=10;2024-11-18 13:27:08',
    'results/Greedy/dronesAmount=8;cellSize=10;2024-11-18 12:22:07'
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

def get_analysis_data(interest, grids_data, folder, global_df):
    interest[0].append(interest[0][-1])
    average_interest_list = []

    for i in range(len(interest[0])):
        total = 0
        for j in range(len(interest)):
            if isinstance(interest[j][i], (int, float)):  # Check if the type is int or float
                total += interest[j][i]
        average_interest_list.append(total / len(interest))

    average_interest = sum(average_interest_list) / len(average_interest_list)

    volatility = 0
    for i in range(len(average_interest_list)):
        volatility += (average_interest_list[i] - average_interest)**2
    volatility = math.sqrt(volatility / len(average_interest_list))
    

    analysis_data = {
        'average_interest': average_interest,
        'average_interest_per_cell': average_interest / grids_data[0]['cells_amount'],
        'volatility': volatility,
        'folder': folder
    }

    # Add data to the global DataFrame with folder name as index
    df_dictionary = pd.DataFrame([analysis_data])
    global_df = pd.concat([global_df, df_dictionary], ignore_index=True)


    return analysis_data, average_interest_list, global_df

def get_grids_average_data(grids_data):
    growth_sums = [grid['growth_sum'] for grid in grids_data]
    average_growth_sum = sum(growth_sums) / len(growth_sums)

    cells_amounts = [grid['cells_amount'] for grid in grids_data]
    average_cells_amount = sum(cells_amounts) / len(cells_amounts)

    heights = [grid['grid_height'] for grid in grids_data]
    average_height = sum(heights) / len(heights)

    widths = [grid['grid_width'] for grid in grids_data]
    average_width = sum(widths) / len(widths)

    grids_average_data = {
        'average_growth_sum': average_growth_sum,
        'average_cells_amount': average_cells_amount,
        'average_height': average_height,
        'average_width': average_width,
        'average_growth_sum_per_cell': average_growth_sum / average_cells_amount
    }

    return grids_average_data

def analyze_data(folder, global_df):
    # print('Current folder:', folder)

    interest, grids_data, meta_data = read_all_data(folder)

    # print('Interest len', len(interest))
    
    flattended_interest = [item for sublist in interest[0:] for item in sublist]

    analysis_data, average_interest_list, global_df = get_analysis_data(interest, grids_data, folder, global_df)
    grids_average_data = get_grids_average_data(grids_data)

    analysis_data_file = f'./{folder}/analysis_data.json'
    grids_average_data_file = f'./{folder}/grids_average_data.json'

    with open(analysis_data_file, 'w') as file:
        json.dump(analysis_data, file, indent=4)

    with open(grids_average_data_file, 'w') as file:
        json.dump(grids_average_data, file, indent=4)

    # print('Analysis Data:', analysis_data)
    # print('Grids Average Data:', grids_average_data)

    # print('Plotting the graph...')
    plt.plot(average_interest_list)
    plt.xlabel('Ітерація')
    plt.ylabel('Сума інтересу')
    # plt.title('Average Cells Sum Over Time')
    plt.grid(True)
    # plt.show()
    # Save plots to a file
    # print('Saving the plot to a file...')
    plot_file = f'./{folder}/plot.png'
    plt.savefig(plot_file)

    plt.clf()  # Clear the current figure

    plt.plot(flattended_interest)
    plt.xlabel('Ітерація')
    plt.ylabel('Сума інтересу')
    plt.grid(True)
    plot_file = f'./{folder}/flattended_plot.png'
    plt.savefig(plot_file)

    plt.clf()  # Clear the current figure

    return global_df


def compare_data(folder1, folder2, folder3, name, global_df):
    interest1, grids_data1, meta_data1 = read_all_data(folder1)
    interest2, grids_data2, meta_data2 = read_all_data(folder2)
    interest3, grids_data3, meta_data3 = read_all_data(folder3)

    _, average_interest_list1, global_df = get_analysis_data(interest1, grids_data1, folder1, global_df)
    _, average_interest_list2, global_df = get_analysis_data(interest2, grids_data2, folder2, global_df)
    _, average_interest_list3, global_df = get_analysis_data(interest3, grids_data3, folder3, global_df)

    # Print difference in average interest in percentage relatively to second folder
    average_interest1 = sum(average_interest_list1) / len(average_interest_list1)
    average_interest2 = sum(average_interest_list2) / len(average_interest_list2)
    average_interest3 = sum(average_interest_list3) / len(average_interest_list3)

    print('Difference in average interest 1:', (average_interest1 - average_interest2) / average_interest2 * 100, '%')
    print('Difference in average interest 3:', (average_interest3 - average_interest2) / average_interest2 * 100, '%')


    label1 = 'Кластеризаційний алгоритм на основі K-Means'
    label2 = 'Алгоритм рівномірного поділу простору '
    label3 = 'Алгоритм рівних ділянок інтересу'

    print('Plotting the comparison graph...')
    plt.plot(average_interest_list1, label=f'{label1}')
    plt.plot(average_interest_list2, label=f'{label2}')
    plt.plot(average_interest_list3, label=f'{label3}')
    plt.xlabel('Ітерація')
    plt.ylabel('Сума інтересу')
    plt.legend()
    plt.grid(True)
    print('Saving the comparison plot to a file...')
    plot_file = './results/comparison_plot_' +name+ '.png'
    plt.savefig(plot_file)
    plt.clf()  # Clear the current figure

    return global_df


# for folder in cluster:
#     global_df = analyze_data(folder, global_df)

# for folder in equal_areas:
#     global_df = analyze_data(folder, global_df)

# for folder in equal_interest:
#     global_df = analyze_data(folder, global_df)

# for folder in greedy:
#     global_df = analyze_data(folder, global_df)

global_df = analyze_data(greedy[3], global_df)

# print(global_df)

# # Save the global DataFrame to a CSV file


# folder_number = 3

# folder1 = cluster[folder_number]
# folder2 = equal_areas[folder_number]
# folder3 = equal_interest[folder_number]

# global_df = compare_data(folder1, folder2, folder3, 'drones=4-float', global_df)

global_df.to_csv('./results/analysis_data_greedy_float.csv', index=False)