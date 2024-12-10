# implement search algorithm
import copy
import os


class Stone():
    def __init__(self, pos, weight) -> None:
        self.pos = pos
        self.weight = weight

    def __eq__(self, other):
        return self.pos == other.pos and self.weight == other.weight


class State():
    def __init__(self, stones, pos_ares, matrix):
        self.stones = stones
        self.pos_ares = pos_ares
        self.matrix = matrix

    def __eq__(self, other):
        if other.pos_ares == -1:
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])):
                    if self.matrix[i][j] != other.matrix[i][j] and self.matrix[i][j] != "@":
                        return False
            return True
        if self.pos_ares != other.pos_ares:
            return False
        for i in range(len(self.stones)):
            if self.stones[i] != other.stones[i]:
                return False
        return True

    def __hash__(self) -> int:
        result = str(self.pos_ares)
        for s in self.stones:
            result += str(s.pos) + str(s.weight)
        return hash(result)


class Node():
    def __init__(self, State, Action, Parent, Weight) -> None:
        self.state = State
        self.action = Action
        self.parent = Parent
        self.weight = Weight


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class SolutionDFS():
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.weight = list()
        self.matrix = list()
        with open(filepath) as ifile:
            weight = ifile.readline().split(" ")
            self.weight = [int(i) for i in weight]
            self.matrix = [list(line) for line in ifile.readlines()]

        goal_matrix = [arr[:] for arr in self.matrix]
        # Create stone objects and get ares position
        w = 0
        stones = []
        goal = []
        pos = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == "$":
                    stones.append(Stone(pos=(i, j), weight=self.weight[w]))
                    w += 1
                    goal_matrix[i][j] = ' '
                elif self.matrix[i][j] == "@":
                    pos = (i, j)
                    goal_matrix[i][j] = ' '
                elif self.matrix[i][j] == ".":
                    goal.append(Stone(pos=(i, j), weight=0))
                    self.matrix[i][j] = ' '
                    goal_matrix[i][j] = '$'

        self.start_state = State(
            stones=stones, pos_ares=pos, matrix=self.matrix)

        self.goal_state = State(stones=goal, pos_ares=-1, matrix=goal_matrix)
        self.solution = None
        self.num_explored = 0

    def actions(self, state):
        x, y = state.pos_ares
        candidates = [
            ("L", x, y-1, x, y - 2),
            ("R", x, y+1, x, y + 2),
            ("U", x-1, y, x - 2, y),
            ("D", x+1, y, x + 2, y)
        ]
        result = []
        for c in candidates:
            if state.matrix[c[1]][c[2]] not in ("#", "$"):
                newMatrix = [arr[:] for arr in state.matrix]
                newMatrix[x][y] = " "
                newMatrix[c[1]][c[2]] = "@"
                pos = (c[1], c[2])
                result.append(
                    (c[0], State(stones=state.stones, pos_ares=pos, matrix=newMatrix), 0))
            elif state.matrix[c[1]][c[2]] == "$" and state.matrix[c[3]][c[4]] not in ("#", "$"):
                stones = copy.deepcopy(state.stones)
                weight = 0
                for s in stones:
                    if s.pos == (c[1], c[2]):
                        s.pos = (c[3], c[4])
                        weight = s.weight
                        break
                newMatrix = [arr[:] for arr in state.matrix]
                newMatrix[x][y] = " "
                newMatrix[c[1]][c[2]] = "@"
                newMatrix[c[3]][c[4]] = "$"
                pos = (c[1], c[2])
                result.append(
                    (c[0], State(stones=stones, pos_ares=pos, matrix=newMatrix), weight))
        return result

    def DeepFirstSearch(self):
        self.num_explored = 0

        # initialize frontier to just the starting position
        start_node = Node(State=self.start_state,
                          Action=None, Parent=None, Weight=0)
        frontier = StackFrontier()
        frontier.add(start_node)

        # initialize an empty explored set
        self.explored = set()

        # keep looping until solution found
        while True:
            # if nothing left in frontier, then no path
            if frontier.empty():
                return None, 0, 0, None

            # choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # if node is the goal, then we have solution
            if node.state == self.goal_state:
                actions = ""
                weight = node.weight
                cur_maze = node.state.matrix
                # follow parents node to find solution
                while node.parent is not None:
                    actions += node.action
                    node = node.parent
                actions = actions[::-1]
                return (actions, self.num_explored, weight, cur_maze)

            # mark node as explored
            self.explored.add(node.state)
            # add neighbors to frontier
            for action, state, weight in self.actions(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(State=state, Parent=node,
                                 Action=action, Weight=node.weight + weight)
                    frontier.add(child)
