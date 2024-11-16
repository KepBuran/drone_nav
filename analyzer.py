import json

grids_data_file = './results/EqualInterest/dronesAmount=2;cellSize=5;2024-11-16 23:58:55/meta_data.json'
interest_file = './results/EqualInterest/dronesAmount=2;cellSize=5;2024-11-16 23:58:55/interest.json'

# Parse the interest file
with open(interest_file, 'r') as file:
    parsed_interest = json.load(file)

print(parsed_interest)

# Parse the grids data file
with open(grids_data_file, 'r') as file:
    parsed_dict = json.load(file)

print(parsed_dict)