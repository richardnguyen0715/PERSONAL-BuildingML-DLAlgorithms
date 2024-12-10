from Libraries import *
# from BFS_Source import *
'''
@param: no.
@return: the memory was used by the program
'''


def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 * 1024)  # megabytes (MB)


'''
@param: no
@return:
    1. the maze.
    2. ares positions.
    3. stone positions.
    4. switch positions.
'''
# Reading frome file


def read_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()

    # Remove the leading and trailing ( space ) and push into a list
    stone_weights = list(map(int, lines[0].strip().split()))

    maze = [list(line.rstrip()) for line in lines[1:]]  # Get the maze

    ares_point = ()

    stone_points = {}

    switch_points = []

    r_len = len(maze)

    c_len = len(maze[0])

    i = 0

    for row in range(r_len):
        for col in range(c_len):
            if maze[row][col] == '$':
                stone_points[(row, col)] = stone_weights[i]
                i += 1
            elif maze[row][col] == '@':
                ares_point = (row, col)
            elif maze[row][col] == '.':
                switch_points.append((row, col))
            elif maze[row][col] == '*':
                stone_points[(row, col)] = stone_weights[i]
                i += 1
                switch_points.append((row, col))
            elif maze[row][col] == '+':
                ares_point = (row, col)
                switch_points.append((row, col))

    if len(stone_points) != len(stone_weights):
        raise "Wrong input file! - please check the number of stone!"

    return maze, ares_point, stone_points, switch_points


def create_file_path():
    current_directory = Path(__file__)
    parent_directory = current_directory.parent
    # Testing the read_input_file method
    filename = str(parent_directory)
    return filename


def to_output_file(filename, path, step, nodes, weight, time, memory, algorithm, ID):
    if ID == 0:
        with open(filename, 'w+') as file:
            if path is None:
                file.write(algorithm + '\n')
                file.write(f'No solution, Time(ms): {
                    round(time*1000, 4)}, Memory(MB): {memory}\n')
                return
            else:
                file.write(algorithm + '\n')
                file.write(f'Steps: {step}, Weight: {weight}, Node: {nodes}, Time(ms): {
                    round(time*1000, 4)}, Memory(MB): {memory}\n')
                file.write(path + '\n')
    else:
        with open(filename, 'a') as file:
            if path is None:
                file.write(algorithm + '\n')
                file.write(f'No solution, Time(ms): {
                    round(time*1000, 4)}, Memory(MB): {memory}\n')
                return
            else:
                file.write(algorithm + '\n')
                file.write(f'Steps: {step}, Weight: {weight}, Node: {nodes}, Time(ms): {
                    round(time*1000, 4)}, Memory(MB): {memory}\n')
                file.write(path + '\n')
