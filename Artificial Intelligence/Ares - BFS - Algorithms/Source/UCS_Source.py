import heapq
import time
import tracemalloc

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


class AresGame:

    def __init__(self, maze, stone_weights):
        self.maze = maze
        self.stone_weights = stone_weights
        self.maze_rows = len(maze)
        self.maze_cols = len(maze[0])
        self.initial_ares, self.initial_stones, self.switches = (
            self.get_initial_positions()
        )

    def get_initial_positions(self):
        ares_pos = None
        stones = []
        switches = []
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

    def is_deadlock(self, stones):

        stones_set = set(stones)
        for stone in stones_set:

            if stone in self.switches:
                continue

            if self.is_corner_deadlock(stone):
                return True

        return False

    def is_corner_deadlock(self, stone_pos):

        x, y = stone_pos
        corners = [
            ((x - 1, y), (x, y - 1)),
            ((x - 1, y), (x, y + 1)),
            ((x + 1, y), (x, y - 1)),
            ((x + 1, y), (x, y + 1)),
        ]

        for wall1, wall2 in corners:
            if (
                not self.is_in_map(wall1[0], wall1[1])
                or self.maze[wall1[0]][wall1[1]] == "#"
            ) and (
                not self.is_in_map(wall2[0], wall2[1])
                or self.maze[wall2[0]][wall2[1]] == "#"
            ):
                return True

        return False

    def is_in_map(self, x, y):
        if 0 <= x < self.maze_rows and 0 <= y < self.maze_cols:
            return True
        return False

    def is_valid_move(self, x, y, stones):
        return self.maze[x][y] != "#" and (x, y) not in stones

    def get_neighbors(self, ares_pos, stones):
        neighbors = []
        ax, ay = ares_pos

        for direction, (dx, dy) in DIRECTIONS.items():
            updated_ax, updated_ay = ax + dx, ay + dy

            # If neighbor is out of map or neighbor is a wall, continue
            if (
                self.is_in_map(updated_ax, updated_ay) == False
                or self.maze[updated_ax][updated_ay] == "#"
            ):
                continue

            # if neighbor is a stone
            if (updated_ax, updated_ay) in stones:

                stone_index = stones.index((updated_ax, updated_ay))
                updated_stone_x, updated_stone_y = updated_ax + dx, updated_ay + dy

                if self.is_in_map(
                    updated_stone_x, updated_stone_y
                ) and self.is_valid_move(updated_stone_x, updated_stone_y, stones):

                    new_stones = list(stones)
                    new_stones[stone_index] = (updated_stone_x, updated_stone_y)
                    cost = (
                        self.stone_weights[stone_index] + 1
                    )  # Cost is based on stone weight and path cost
                    neighbors.append(
                        (
                            (updated_ax, updated_ay),
                            tuple(new_stones),
                            direction.upper(),
                            cost,
                        )
                    )

            elif self.is_valid_move(updated_ax, updated_ay, stones):
                # Move without pushing
                neighbors.append(
                    ((updated_ax, updated_ay), tuple(stones), direction.lower(), 1)
                )

        return neighbors

    def uniform_cost_search(self):

        expanded_nodes = 0

        # path_cost, ares_position, stones, paths, total_weight_pushed
        initial_state = (0, self.initial_ares, tuple(self.initial_stones), "")
        frontier = [initial_state]

        frontier_states = {(self.initial_ares, tuple(self.initial_stones)): 0}

        explored_set = set()

        while frontier:

            # Pop node have lowest path cost, current node is used for checking if current node is in frontier or explored set.
            cost, ares_pos, stones, path = heapq.heappop(frontier)
            current_state = (ares_pos, tuple(sorted(stones)))

            if current_state in frontier_states:
                del frontier_states[current_state]

            if self.is_goal(stones):
                total_weights = cost - len(path)
                return (path, expanded_nodes, total_weights)

            explored_set.add(current_state)

            for (
                new_ares_pos,
                new_stones,
                move_direction,
                move_cost,
            ) in self.get_neighbors(ares_pos, stones):

                if self.is_deadlock(new_stones):
                    continue

                new_cost = cost + move_cost

                child_state = (new_ares_pos, tuple(sorted(new_stones)))

                if child_state in explored_set:
                    continue

                if child_state in frontier_states:
                    if new_cost < frontier_states[child_state]:

                        frontier = [
                            (cost, ares_pos, stones, path)
                            for cost, ares_pos, stones, path in frontier
                            if (ares_pos, tuple(sorted(stones))) != child_state
                        ]
                        heapq.heapify(frontier)

                        heapq.heappush(
                            frontier,
                            (new_cost, new_ares_pos, new_stones, path + move_direction),
                        )

                        frontier_states[child_state] = new_cost
                else:
                    expanded_nodes += 1
                    heapq.heappush(
                        frontier,
                        (new_cost, new_ares_pos, new_stones, path + move_direction),
                    )

                    frontier_states[child_state] = new_cost

        return (
            None,
            float("inf"),
            float("inf")
        )  # No solution found
