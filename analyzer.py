import ast

grids_data_file = './results/EqualInterest/GRIDS_DATA_drones_amount=4_cell_size=10_2024-11-16 22:43:55.txt'

interest_file = './results/EqualInterest/INTEREST_drones_amount=4_cell_size=10_2024-11-16 22:43:55.txt'


parsed_interest = []
# Read the file and parse the contents
with open(interest_file, 'r') as file:
    for line in file:
        # Split the line by commas and convert each element to a float
        parsed_line = [float(value) for value in line.strip().split(',') if value]
        # Append the parsed line to the list
        parsed_interest.append(parsed_line)

# print(parsed_interest)

# Read the file and parse the dictionary
with open(grids_data_file, 'r') as file:
    data = file.read()
    parsed_dict = ast.literal_eval(data)

print(parsed_dict)