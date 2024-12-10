 
def read_input_file(filename):
    maze = []  #ma trận
    stones_weight = []
    current_row = []
    num_of_stones = 0
    num_of_switches = 0
    CHARACTERS = {"#", " ", "$", "+", "*", ".", "@"}
    try:
        with open(filename, "r") as file:
            list_weight = file.readline().strip()
            stones_weight = list(map(int, list_weight.split()))

            while True:
                char = file.read(1)
                if not char:
                    if current_row:
                        maze.append(current_row)
                    break

                if char == "\n":
                    maze.append(current_row)
                    current_row = []
                elif char in CHARACTERS:
                    if char == "$":
                        num_of_stones += 1
                    elif char == "+":
                        num_of_switches += 1
                    elif char == "*":
                        num_of_stones += 1
                        num_of_switches += 1
                    elif char == ".":
                        num_of_switches += 1
                    current_row.append(char)
                else:
                    print(f"Invalid character found: '{char}'")
                    return None  # Thông báo ký tự không hợp lệ

            if num_of_stones != num_of_switches:
                print(f"Error: The number of stones and switches should be equal.")
                return None

            cols = 0
            for row in maze:
                if(len(row) > cols):
                    cols = len(row)
            for i in range(len(maze)):
                maze[i] = maze[i] + [' '] * (cols - len(maze[i]))

        return stones_weight, maze

    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None
    except IOError:
        print("Error: Unable to read from file.")
        return None
    
def print_output(path, total_weight, nodes, time, memory, filename='output.txt'):
    with open(filename, 'w') as f:
        f.write("A* Search\n")
        f.write(f"Steps: {len(path)}, ")
        f.write(f"Weight: {total_weight}, ")
        f.write(f"Node: {nodes} ")
        f.write(f"Time (ms): {time:.2f}, ")
        f.write(f"Memory (MB): {memory:.2f}\n")
        f.write(f"{path}\n")

def create_output_name(inputFileName):
    result = inputFileName.replace("input","output")
    return result

  