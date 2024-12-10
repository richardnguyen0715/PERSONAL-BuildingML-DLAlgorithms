from FileHandling import *
from AStarSearching import *
from GUI import *
from pathlib import Path

current_directory = Path.cwd()
parent_directory = current_directory.parent
# Testing the `read_input_file` method
inputFileName = "input_02.txt"
filename = str(parent_directory) + "/input/" + inputFileName
stone_weights, maze = read_input_file(filename)

solver = AStarSearching(maze, stone_weights)

path, total_cost, time, nodes, memory, total_weight = solver.a_star_search()

print(path)
if path:
     print_output(path, total_weight, nodes, time, memory,create_output_name(inputFileName))
     player_path = list(path.upper())
     game = Game(maze, player_path, stone_weights)
     game.run()
else:
     print("No solution found.")


