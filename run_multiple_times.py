import os
import subprocess

# List of different INIT_DRONES_AMOUNT values
drones_amount_list = [2, 4, 8]
algorithm_names = ['EqualInterest', 'EqualAreas', 'Cluster']

for algorithm_name in algorithm_names:
    for drones_amount in drones_amount_list:
        # Set the environment variable
        env = os.environ.copy()
        env['INIT_DRONES_AMOUNT'] = str(drones_amount)
        env['ALGORITHM_NAME'] = algorithm_name
        
        print(f"@@@@@@@@@@@@@@Running the script with INIT_DRONES_AMOUNT={drones_amount} and ALGORITHM_NAME={algorithm_name}")

        # Run the main script and wait for it to finish
        result = subprocess.run(['python3', 'main.py'], env=env)
        
        # Check if the subprocess completed successfully
        if result.returncode != 0:
            print(f"Error: The script failed with return code {result.returncode}")