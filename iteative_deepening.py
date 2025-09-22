import pandas as pd

try:
    table = pd.read_csv('input.txt', sep=r"\s+", skiprows=1, header=None) 
    with open('input.txt', 'r') as file:
        command = file.readline().split()
except:
    print("Error reading input.txt")
    exit(0)

goal_state = int(command[0])
search = command[1]

all_tasks = table[0].tolist()
task_data = {}
for i, task in enumerate(all_tasks):
    task_data[task] = {
        'value': table[1][i],
        'length': table[2][i],
        'deadline': table[3][i]
    }

def calculate_true_value(path, data):
    if not path:
        return 0
    
    total_value = 0
    current_time = 0

    for task_name in path:
        task = data[task_name]
        current_time += task['length']

        if current_time <= task['deadline']:
            total_value += task['value']

    return total_value

def calculate_deadline(path, data):
    if not path:
        return True
    
    length = 0

    for task in path:
        length += data[task]['length']

    if length > task_data[path[-1]]['deadline']:
        return False
    
    return True

def ids(current_path, depth_limit):
    if search == "V" and current_path:
        value = calculate_true_value(current_path, task_data) 
        print(f"{' '.join(current_path)} Value={value}")

    if calculate_true_value(current_path, task_data) >= goal_state:
        return current_path
    
    if len(current_path) >= depth_limit:
        return "cutoff"
    
    was_cutoff = False
    for task in all_tasks:
        if task not in current_path:
            new_path = current_path + [task]

            if calculate_deadline(new_path, task_data):
                result = ids(new_path, depth_limit)

                if isinstance(result, list):
                    return result
                
                if result == "cutoff":
                    was_cutoff = True

    return "cutoff" if was_cutoff else None

for depth in range(1, len(all_tasks) + 1):
    if search == "V":
        print(f"\nDepth={depth}")

    result = ids([], depth)

    if type(result) == list:
        print(f"\nFound solution {' '.join(result)}. Value={calculate_true_value(result, task_data)}")
        break
    
    if result is None:
        print("\nNo solution found")
        break