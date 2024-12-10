import heapq
import time
import tracemalloc

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


class AStarSearching:

    def __init__(self, maze, stone_weights):
        self.maze = maze
        self.stone_weights = stone_weights
        self.maze_rows = len(maze)
        self.maze_cols = len(maze[0])
        self.initial_ares, self.initial_stones, self.switches = self.get_initial_positions()

    def get_initial_positions(self):
        ares_pos = None
        stones = []
        switches = []
        stone_idx = 0
        for i in range(self.maze_rows):
            for j in range(self.maze_cols):
                if self.maze[i][j] == "*":
                    switches.append((i, j))
                    stones.append((i, j))
                elif self.maze[i][j] == ".":
                    switches.append((i, j))
                elif self.maze[i][j] == "@":
                    ares_pos = (i, j)
                elif self.maze[i][j] == "$":
                    stones.append((i, j))
                elif self.maze[i][j] == "+":
                    switches.append((i, j))
                    ares_pos = (i, j)
        return ares_pos, stones, switches

    def is_goal(self, stones):
        return all(stone in self.switches for stone in stones)
    # list comprehension

    def is_in_map(self, x, y):
        return 0 <= x < self.maze_rows and 0 <= y < self.maze_cols

    def is_valid_move(self, x, y, stones):
        return self.maze[x][y] != "#" and (x, y) not in stones

    def get_neighbors(self, ares_pos, stones):
        # Hàm cho ares đi 4 hướng và cập nhật trạng thái của đá, ares, giá trị bước đi
        neighbors = []
        ax, ay = ares_pos

        for direction, (dx, dy) in DIRECTIONS.items():
            # direction nhận key, (dx,dy) nhận value
            updated_ax, updated_ay = ax + dx, ay + dy
            # Hướng đi của Ares
            # If neighbor is out of map or neighbor is a wall, continue
            if not self.is_in_map(updated_ax, updated_ay) or self.maze[updated_ax][updated_ay] == "#":
                continue

            # If neighbor is a stone
            if (updated_ax, updated_ay) in stones:
                stone_index = stones.index((updated_ax, updated_ay))
                # Lấy index của stone trong mảng stones
                updated_stone_x, updated_stone_y = updated_ax + dx, updated_ay + dy
                # Vị trí stone chắc chắn khác, nhưng cần kiểm tra với các stone khác

                if self.is_in_map(updated_stone_x, updated_stone_y) and self.is_valid_move(updated_stone_x, updated_stone_y, stones):
                    new_stones = list(stones)
                    new_stones[stone_index] = (
                        updated_stone_x, updated_stone_y)
                    # Cost is based on stone weight
                    cost = self.stone_weights[stone_index]
                    neighbors.append((updated_ax, updated_ay, tuple(
                        new_stones), direction.upper(), cost+1))
            elif self.is_valid_move(updated_ax, updated_ay, stones):
                # Move without pushing
                neighbors.append(
                    (updated_ax, updated_ay, tuple(stones), direction.lower(), 1))
        return neighbors

    def is_deadlocked(self, stones):
        """Check for deadlock conditions for each stone position.
           A stone is in deadlock if it is in a corner or an unmovable position that prevents it from reaching any switch."""
        for stone in stones:
            x, y = stone

            # Check if the stone is already on a switch; if so, it's not a deadlock
            if stone in self.switches:
                continue

            # Deadlock check: if the stone is in a corner or trapped position
            # Example: check if a stone is against walls or in an edge position where it cannot be moved to a switch.

            # Check corner deadlock: stone is surrounded by walls in two adjacent directions
            if (self.is_in_map(x + 1, y) and self.maze[x + 1][y] == "#") and (
                    self.is_in_map(x, y + 1) and self.maze[x][y + 1] == "#"):
                return True
            if (self.is_in_map(x - 1, y) and self.maze[x - 1][y] == "#") and (
                    self.is_in_map(x, y - 1) and self.maze[x][y - 1] == "#"):
                return True
            if (self.is_in_map(x + 1, y) and self.maze[x + 1][y] == "#") and (
                    self.is_in_map(x, y - 1) and self.maze[x][y - 1] == "#"):
                return True
            if (self.is_in_map(x - 1, y) and self.maze[x - 1][y] == "#") and (
                    self.is_in_map(x, y + 1) and self.maze[x][y + 1] == "#"):
                return True

        return False

    def heuristic(self, stones):
        # Calculate the minimum distance for each stone to any switch
        # Tính tổng khoảng cách nhỏ nhất
        # Ares_to_stone_distances = []
        # Ares_to_stone_distance =0
        # for stone in stones:
        #     if stone not in self.switches:
        #        Ares_to_stone_distances.append(abs(Ares[0]-stone[0]) + abs(Ares[1]-stone[1]))
        #
        # if not Ares_to_stone_distances:
        #     Ares_to_stone_distance = 0
        # else:
        #     Ares_to_stone_distance = min(Ares_to_stone_distances)
        total_distance = 0
        for index, stone in enumerate(stones):
            min_distance = min(
                abs(stone[0] - switch[0]) + abs(stone[1] - switch[1]) for switch in self.switches)
            total_distance += min_distance * \
                self.stone_weights[index]  # Nhân với khối lượng đá
        return total_distance

    def a_star_search(self):

        tracemalloc.start()  # Tính dung lượng bộ nhớ
        start_time_1 = time.time()  # Tính thời gian
        nodes = 0

        #f, path_cost, ares_position, stones, paths, total_weight_pushed
        frontier = [(0 + self.heuristic(self.initial_stones), 0, self.initial_ares, tuple(self.initial_stones), "", 0)]

        frontier_nodes = {(self.initial_ares, tuple(self.initial_stones)): 0}

        explored_set = set()

        while frontier:

            # Pop node with lowest f = g + h
            _, cost, ares_pos, stones, path, weight_pushed = heapq.heappop(
                frontier)
            current_node = (ares_pos, tuple(sorted(stones)))

            if current_node in frontier_nodes:
                del frontier_nodes[current_node]

            if self.is_goal(stones):
                end_time_1 = time.time()
                memory, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                time_running = end_time_1 - start_time_1
                return path, cost, time_running, nodes, memory / (1024 * 1024), weight_pushed

            explored_set.add(current_node)

            for new_ax, new_ay, new_stones, move_direction, move_cost in self.get_neighbors(ares_pos, stones):
                # Skip if new state is in deadlock
                if self.is_deadlocked(new_stones):
                    continue

                child_node = (new_ax, new_ay, tuple(sorted(new_stones)))
                if child_node in explored_set:
                    continue

                new_cost = cost + move_cost

                # Update weight pushed if moving a stone
                new_weight_pushed = weight_pushed
                if move_direction.isupper():
                    new_weight_pushed += move_cost-1

                heuristic_cost = self.heuristic(new_stones)
                f_cost = new_cost + heuristic_cost


                if child_node in frontier_nodes:
                    if f_cost < frontier_nodes[child_node]:
                        # Update frontier with better cost
                        frontier = [
                            (f, c, pos, s, p, wp) for f, c, pos, s, p, wp in frontier
                            if (pos, tuple(sorted(s))) != child_node
                        ]
                        heapq.heapify(frontier)
                        heapq.heappush(frontier, (f_cost, new_cost, (new_ax, new_ay),
                                       new_stones, path + move_direction, new_weight_pushed))
                        frontier_nodes[child_node] = f_cost
                else:
                    nodes += 1
                    heapq.heappush(frontier, (f_cost, new_cost, (new_ax, new_ay),
                                   new_stones, path + move_direction, new_weight_pushed))
                    frontier_nodes[child_node] = f_cost


        # No solution found
        memory, peak = tracemalloc.get_traced_memory()
        end_time_1= time.time()
        tracemalloc.stop()
        time_running = end_time_1 - start_time_1
        return None, float("inf"), time_running, float("inf"), memory / (1024 * 1024), float("inf")
