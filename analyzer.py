import json

cluster = [
    'results/Cluster/dronesAmount=2;cellSize=5;2024-11-17 10:32:21',
    'results/Cluster/dronesAmount=4;cellSize=5;2024-11-17 12:01:33'
    'results/Cluster/dronesAmount=8;cellSize=5;2024-11-17 13:50:25'
]

equal_areas = [
    'results/EqualAreas/dronesAmount=2;cellSize=5;2024-11-17 06:04:50',
    'results/EqualAreas/dronesAmount=4;cellSize=5;2024-11-17 07:36:17'
    'results/EqualAreas/dronesAmount=8;cellSize=5;2024-11-17 09:05:48'
]

equal_interest = [
    'results/EqualInterest/dronesAmount=2;cellSize=5;2024-11-17 01:37:53',
    'results/EqualInterest/dronesAmount=4;cellSize=5;2024-11-17 03:05:10'
    'results/EqualInterest/dronesAmount=8;cellSize=5;2024-11-17 04:35:17'
]

current_folder = cluster[0]

grids_data = 
interest_file = './results/EqualInterest/dronesAmount=2;cellSize=5;2024-11-16 23:58:55/interest.json'

# Parse the interest file
with open(interest_file, 'r') as file:
    parsed_interest = json.load(file)

print(parsed_interest)

# Parse the grids data file
with open(grids_data_file, 'r') as file:
    parsed_dict = json.load(file)

print(parsed_dict)