import pandas as pd
import random

try:
    table = pd.read_csv('input.txt', sep=r"\s+", skiprows=1, header=None) 
    with open('input.txt', 'r') as file:
        command = file.readline().split()
except:
    print("Error reading input.txt")
    exit(0)

goal_state = int(command[0])
search = command[1]
restarts = int(command[2])

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

def generate_random_start_state():
    sub_tasks = []

    for task in all_tasks:
        if random.random() < 0.5:
            sub_tasks.append(task)

    random.shuffle(sub_tasks)

    return sub_tasks

def calculate_error(current_path):
    if not current_path:
        return goal_state
    
    true_value = calculate_true_value(current_path, task_data)
    error = max(0, goal_state - true_value)

    return error

def generate_neighbors(current_path):
    all_neighbors = []

    for i in range(len(current_path)):
        neighbor = current_path[:i] + current_path[i+1:]
        all_neighbors.append(neighbor)

    for i in range(len(current_path) - 1):
        neighbor = list(current_path)
        neighbor[i], neighbor[i+1] = neighbor[i+1], neighbor[i]
        all_neighbors.append(neighbor)

    for task in all_tasks:
        if task not in current_path:
            neighbor = current_path + [task]
            all_neighbors.append(neighbor)

    unique_tuples = set(tuple(path) for path in all_neighbors)
    unique_neighbors = [list(path_tuple) for path_tuple in unique_tuples]

    return unique_neighbors

def hill_climbing(restarts):
    for i in range(restarts):
        current_path = generate_random_start_state()
        is_first = True

        while True: 
            current_value = calculate_true_value(current_path, task_data)
            current_error = calculate_error(current_path)

            if search == "V":
                if is_first:
                    print(f"\nRandomly chosen start state: {' '.join(current_path)} Value={current_value}. Error={current_error}.")
                    is_first = False

                else:
                    print(f"\nMove to {' '.join(current_path)} Value={current_value}. Error={current_error}.")

            neighbors = generate_neighbors(current_path)

            if search == "V":
                print("Neighbors")

            best_neighbor = None
            min_error = current_error

            for n in neighbors:
                neighbor_val = calculate_true_value(n, task_data)
                neighbor_error = calculate_error(n)

                if search == "V":
                    if neighbor_error == 0:
                        print(f"{' '.join(n) if n else '{}'} Value={neighbor_val}. Error={neighbor_error}. Success!")

                    else:
                        print(f"{' '.join(n) if n else '{}'} Value={neighbor_val}. Error={neighbor_error}.")

                if neighbor_error == 0:
                    print(f"\nFound solution {' '.join(n)}. Value={neighbor_val}.")
                    return
                
                if neighbor_error < min_error:
                    min_error = neighbor_error
                    best_neighbor = n

            if best_neighbor is not None:
                current_path = best_neighbor

            else:
                if search == "V":
                    print("\nSearch failed.")

                break 
    print("No solution found")
    return None

if restarts > 0:
    hill_climbing(restarts)
else:
    print("Number of restarts must be greater than or equal to 0")
    exit(0)