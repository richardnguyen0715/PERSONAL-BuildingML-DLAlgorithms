import tracemalloc

import pygame
import time
import os
from BFS_Source import *
from Other_funcs import *
from DFS_Source import SolutionDFS
from UCS_Source import *
from Astart.source.AStarSearching import *
from Astart.source.FileHandling import *
# Game constants
TILE_SIZE = 60
PLAYER_IMAGE = "player.png"
STONE_IMAGE = "stone.png"
WALL_IMAGE = "wall.png"


class Game:
    def __init__(self, maze, player_path, stone_weights):
        pygame.init()
        self.original_maze = maze
        self.original_path = player_path
        self.stone_weights = stone_weights
        self.rows = len(maze)
        self.cols = len(maze[0])

        # Dynamic screen sizing
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h

        # Calculate responsive tile size
        self.tile_size = min(
            (self.screen_width - 40) // self.cols,
            (self.screen_height - 120) // (self.rows + 1)
        )

        # Responsive button and font sizes
        self.button_height = max(30, int(self.tile_size * 0.5))
        self.button_width = max(80, int(self.tile_size * 1.33))
        self.font_size = max(24, int(self.tile_size * 0.4))
        self.stats_font_size = max(18, int(self.tile_size * 0.3))

        # Create screen with full window size
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Responsive Sokoban")

        # Responsive positioning
        button_y = self.rows * self.tile_size + 10
        spacing = max(10, int(self.tile_size * 0.17))

        # Create buttons with responsive sizing
        self.start_button = pygame.Rect(
            10, button_y, self.button_width, self.button_height)
        self.pause_button = pygame.Rect(
            10 + (self.button_width + spacing), button_y,
            self.button_width, self.button_height)
        self.reset_button = pygame.Rect(
            10 + (self.button_width + spacing) * 2, button_y,
            self.button_width, self.button_height)
        self.exit_button = pygame.Rect(
            10 + (self.button_width + spacing) * 3, button_y,
            self.button_width, self.button_height)

        # Initialize fonts with dynamic sizing
        self.font = pygame.font.Font(None, self.font_size)
        self.stats_font = pygame.font.Font(None, self.stats_font_size)

        # Stats tracking
        self.steps_taken = 0
        self.total_push_weight = 0

        # Load images with responsive scaling
        self.load_game_images()

        self.reset_game()

    def load_game_images(self):
        """Load and scale game images to responsive tile size"""
        parent_path = create_file_path()
        self.player_img = pygame.image.load(
            os.path.join(parent_path + r"\assets", PLAYER_IMAGE))
        self.stone_img = pygame.image.load(
            os.path.join(parent_path + r"\assets", STONE_IMAGE))
        self.wall_img = pygame.image.load(
            os.path.join(parent_path + r"\assets", WALL_IMAGE))

        # Scale images to dynamic tile size
        self.player_img = pygame.transform.scale(
            self.player_img, (self.tile_size, self.tile_size))
        self.stone_img = pygame.transform.scale(
            self.stone_img, (self.tile_size, self.tile_size))
        self.wall_img = pygame.transform.scale(
            self.wall_img, (self.tile_size, self.tile_size))

    def handle_resize(self):
        """Handle window resize event"""
        # Recalculate screen dimensions
        self.screen_width = pygame.display.get_surface().get_width()
        self.screen_height = pygame.display.get_surface().get_height()

        # Calculate tile size to fit maze and leave space for buttons/stats
        self.tile_size = min(
            (self.screen_width - 40) // self.cols,
            (self.screen_height - 120) // self.rows
        )

        # Reload images with new tile size
        self.load_game_images()

        # Recalculate button sizes and positions
        self.button_height = max(30, int(self.tile_size * 0.5))
        self.button_width = max(80, int(self.tile_size * 1.33))
        self.font_size = max(24, int(self.tile_size * 0.4))
        self.stats_font_size = max(18, int(self.tile_size * 0.3))

        # Recreate fonts
        self.font = pygame.font.Font(None, self.font_size)
        self.stats_font = pygame.font.Font(None, self.stats_font_size)

        # Calculate maze display area
        maze_display_height = self.rows * self.tile_size
        button_y = maze_display_height + 10

        # Responsive button positioning
        spacing = max(10, int(self.tile_size * 0.17))

        self.start_button = pygame.Rect(
            10, button_y, self.button_width, self.button_height)
        self.pause_button = pygame.Rect(
            10 + (self.button_width + spacing), button_y,
            self.button_width, self.button_height)
        self.reset_button = pygame.Rect(
            10 + (self.button_width + spacing) * 2, button_y,
            self.button_width, self.button_height)
        self.exit_button = pygame.Rect(
            10 + (self.button_width + spacing) * 3, button_y,
            self.button_width, self.button_height)

    def reset_game(self):
        """Reset the game to initial state"""
        self.maze = [list(row) for row in self.original_maze]
        self.player_path = self.original_path
        self.current_path_index = 0
        self.load_positions()
        self.game_started = False
        self.game_paused = False
        self.steps_taken = 0
        self.total_push_weight = 0

    def load_positions(self):
        self.player_pos = None
        self.stones = []
        self.targets = []

        for i, row in enumerate(self.maze):
            for j, char in enumerate(row):
                if char == '@':
                    self.player_pos = [i, j]
                    self.maze[i][j] = ' '
                elif char == '$':
                    self.stones.append([i, j])
                    self.maze[i][j] = ' '
                elif char == '.':
                    self.targets.append((i, j))
                elif char == '*':
                    self.stones.append([i, j])
                    self.targets.append((i, j))
                    self.maze[i][j] = '.'
                elif char == '+':
                    self.player_pos = [i, j]
                    self.maze[i][j] = '.'
                    self.targets.append((i, j))

    def draw_buttons(self):
        # Define colors
        colors = {
            'start': {
                'normal': (100, 255, 100),   # Bright green
                'disabled': (150, 150, 150),  # Gray
                'border': (50, 150, 50)       # Dark green border
            },
            'pause': {
                'normal': (255, 255, 100),   # Yellow
                'paused': (255, 100, 100),   # Red
                'border': (200, 200, 50)     # Dark yellow border
            },
            'reset': {
                'normal': (100, 100, 255),   # Blue
                'border': (50, 50, 150)      # Dark blue border
            },
            'exit': {
                'normal': (150, 150, 150),  # Gray
                'border': (0, 0, 0)           # Black border
            }
        }

        button_y = self.rows * self.tile_size + 10
        button_width = 80
        button_height = 30
        spacing = 20

        # Reposition all buttons including exit
        self.start_button = pygame.Rect(
            20, button_y, button_width, button_height)
        self.pause_button = pygame.Rect(
            20 + (button_width + spacing), button_y, button_width, button_height)
        self.reset_button = pygame.Rect(
            20 + (button_width + spacing) * 2, button_y, button_width, button_height)
        self.exit_button = pygame.Rect(
            20 + (button_width + spacing) * 3, button_y, button_width, button_height)

        # Button drawing function with border
        def draw_button(button, color, text, border_color=None):
            # Draw border
            if border_color:
                border_rect = pygame.Rect(
                    button.x - 2, button.y - 2,
                    button.width + 4, button.height + 4
                )
                pygame.draw.rect(self.screen, border_color, border_rect)

            # Draw button
            pygame.draw.rect(self.screen, color, button)

            # Draw text
            text_surface = self.font.render(text, True, (0, 0, 0))

            # Ensure text fits within button
            if text_surface.get_width() > button.width - 10:
                # If text is too wide, use a smaller font
                small_font = pygame.font.Font(None, 24)
                text_surface = small_font.render(text, True, (0, 0, 0))

            text_rect = text_surface.get_rect(center=button.center)
            self.screen.blit(text_surface, text_rect)

        # Start button
        button_color = (colors['start']['disabled'] if self.game_started
                        else colors['start']['normal'])
        border_color = colors['start']['border']
        draw_button(self.start_button, button_color, "Start", border_color)

        # Pause button
        button_color = (colors['pause']['paused'] if self.game_paused
                        else colors['pause']['normal'])
        border_color = colors['pause']['border']
        pause_text = "Resume" if self.game_paused else "Pause"
        draw_button(self.pause_button, button_color, pause_text, border_color)

        # Reset button
        draw_button(self.reset_button, colors['reset']['normal'],
                    "Reset", colors['reset']['border'])

        # Exit button
        draw_button(self.exit_button, colors['exit']['normal'],
                    "Exit", colors['exit']['border'])

    def draw_stats(self):
        # Draw statistics
        stats_y = self.rows * self.tile_size + 55

        # Steps counter
        steps_text = f"Steps: {self.steps_taken}"
        text = self.stats_font.render(steps_text, True, (0, 0, 0))
        self.screen.blit(text, (20, stats_y))

        # Push weight counter
        weight_text = f"Total Push Weight: {self.total_push_weight}"
        text = self.stats_font.render(weight_text, True, (0, 0, 0))
        self.screen.blit(text, (220, stats_y))

        if (len(self.original_path) == 0):
            no_solution_y = self.rows * self.tile_size + 85
            no_solution_text = f"No solution!"
            text = self.stats_font.render(no_solution_text, True, (0, 0, 0))
            self.screen.blit(text, (20, no_solution_y))

    def draw(self):
        # Fill background with white
        self.screen.fill((255, 228, 168, 255))

        # Calculate center offset for maze
        maze_width = self.cols * self.tile_size
        maze_height = self.rows * self.tile_size
        start_x = (self.screen_width - maze_width) // 2
        start_y = 0  # Start from top

        # Draw maze walls using wall image
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == '#':
                    self.screen.blit(
                        self.wall_img,
                        (start_x + j * self.tile_size,
                         start_y + i * self.tile_size)
                    )

        # Draw targets (red circles)
        for target in self.targets:
            circle_center = (
                start_x + target[1] * self.tile_size + self.tile_size // 2,
                start_y + target[0] * self.tile_size + self.tile_size // 2
            )
            circle_radius = self.tile_size // 4
            pygame.draw.circle(self.screen, (255, 0, 0),
                               circle_center, circle_radius)

        # Draw player with special rendering for targets
        player_x = start_x + self.player_pos[1] * self.tile_size
        player_y = start_y + self.player_pos[0] * self.tile_size

        if self.maze[self.player_pos[0]][self.player_pos[1]] == '+':
            player_surface = self.player_img.copy()
            # Darken the image
            player_surface.fill(
                (0, 0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(player_surface, (player_x, player_y))
        else:
            self.screen.blit(self.player_img, (player_x, player_y))

        # Draw stones with weights and special rendering for targets
        for i, stone in enumerate(self.stones):
            stone_x = start_x + stone[1] * self.tile_size
            stone_y = start_y + stone[0] * self.tile_size

            if (stone[0], stone[1]) in self.targets:
                stone_surface = self.stone_img.copy()
                # Darken the image
                stone_surface.fill(
                    (0, 0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(stone_surface, (stone_x, stone_y))
            else:
                self.screen.blit(self.stone_img, (stone_x, stone_y))

            # Draw stone weight
            weight_text = str(self.stone_weights[i])
            text = self.stats_font.render(weight_text, True, (255, 255, 0))
            text_rect = text.get_rect(center=(
                stone_x + self.tile_size // 2,
                stone_y + self.tile_size // 2
            ))
            self.screen.blit(text, text_rect)

        # Draw buttons and stats
        maze_display_height = self.rows * self.tile_size
        button_y = maze_display_height + 10
        stats_y = maze_display_height + 45

        # Recalculate button positions
        spacing = 10
        self.start_button.y = button_y
        self.pause_button.y = button_y
        self.reset_button.y = button_y
        self.exit_button.y = button_y

        # Draw buttons with adjusted positions
        self.draw_buttons()

        # Draw stats
        self.draw_stats()

        pygame.display.flip()

    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.start_button.collidepoint(pos):
            if not self.game_started:
                self.game_started = True
                self.game_paused = False
            return True
        elif self.pause_button.collidepoint(pos):
            if self.game_started:
                self.game_paused = not self.game_paused
            return True
        elif self.reset_button.collidepoint(pos):
            self.reset_game()
            return True
        elif self.exit_button.collidepoint(pos):
            # You'll need to implement a way to return to the previous screen
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return True
        return False

    def move_player(self, direction):
        dx, dy = {"U": (-1, 0), "D": (1, 0), "L": (0, -1),
                  "R": (0, 1)}[direction]
        new_pos = [self.player_pos[0] + dx, self.player_pos[1] + dy]

        # Check for stone
        stone_idx = None
        for i, stone in enumerate(self.stones):
            if stone[0] == new_pos[0] and stone[1] == new_pos[1]:
                stone_idx = i
                break

        if stone_idx is not None:
            # Calculate new stone position
            new_stone_pos = [new_pos[0] + dx, new_pos[1] + dy]

            # Check if stone can be pushed
            if (self.maze[new_stone_pos[0]][new_stone_pos[1]] != '#' and
                not any(s[0] == new_stone_pos[0] and s[1] == new_stone_pos[1]
                        for s in self.stones)):
                # Move stone and update stats
                self.stones[stone_idx] = new_stone_pos
                self.total_push_weight += self.stone_weights[stone_idx]
                # Move player
                self.player_pos = new_pos
                self.steps_taken += 1
                return True
        else:
            # Move player if no wall
            if self.maze[new_pos[0]][new_pos[1]] != '#':
                self.player_pos = new_pos
                self.steps_taken += 1
                return True
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.handle_click(event.pos):
                            continue
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    self.handle_resize()

            if (self.game_started and not self.game_paused and
                    self.current_path_index < len(self.player_path)):
                # Get next move from path
                direction = self.player_path[self.current_path_index]
                if self.move_player(direction):
                    self.current_path_index += 1

                    # Check win condition
                    if all((stone[0], stone[1]) in self.targets for stone in self.stones):
                        self.game_paused = True

            self.draw()
            clock.tick(4)  # Control animation speed

        # Do not quit Pygame here, allowing for return to the menu

def get_memory_usage_uss():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_full_info()
    return mem_info.uss / (1024 * 1024)  # MB

def open_maze_solver(filepath, algorithm, ID):
    maze, ares_point, stone_points, switch_points = read_file(filepath)
    stone_weight = list(stone_points.values())
    # Solution var:
    # path: a string for the solution path. Ex: LLRLR....
    # nodes: int: total node explored.
    # total_weight: int: total weight.
    # new_maze: Array. The maze after running algorithm
    import time
    path, nodes, total_weight, new_maze = None, 0, 0, None
    if algorithm == 'BFS':
        # BFS algorithm
        # Start search

        start_time = time.time()
        # Search algorithm
        # Đo lượng bộ nhớ trước
        memory_before = get_memory_usage_uss()
        path, nodes, total_weight, new_maze = solve_maze_with_bfs(
            maze, ares_point, stone_points, switch_points)
        memory_after = get_memory_usage_uss()
        memory = (memory_after - memory_before)  # Đổi sang MB
        end_time = time.time()
        time = end_time - start_time
    elif algorithm == 'DFS':
        # DFS init
        dfs = SolutionDFS(filepath)
        # Start search
        start_time = time.time()
        # Đo lượng bộ nhớ trước
        memory_before =get_memory_usage_uss()
        # DFS algorithm
        path, nodes, total_weight, new_maze = dfs.DeepFirstSearch()
        memory_after = get_memory_usage_uss()
        memory = (memory_after - memory_before)   # Đổi sang MB
        end_time = time.time()
        time = end_time - start_time
    elif algorithm == 'UCS':
        # add your solution here
        # start time, memory
        # path, nodes, total_weight, new_maze = your_solution()
        # end time, memory
        solver = AresGame(maze, stone_weight)
        start_time = time.time()
        tracemalloc.start()
        # Đo lượng bộ nhớ trước
        # memory_before = tracemalloc.get_traced_memory()[0]
        memory_before = get_memory_usage_uss()
        path, nodes, total_weight = solver.uniform_cost_search()
        memory_after = get_memory_usage_uss()
        memory = memory_after -memory_before
        # Đo lượng bộ nhớ sau
        # memory_after = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()
        # memory = (memory_after - memory_before) / (1024 * 1024)

        # Đổi sang MB
        end_time = time.time()
        time = end_time - start_time
    elif algorithm == 'A*':
        # add your solution here
        # start time, memory
        # path, nodes, total_weight, new_maze = your_solution()
        # end time, memory
        stone_weights, maze = read_input_file(filepath)

        solver_2 = AStarSearching(maze, stone_weights)

        path, total_cost, time, nodes, memory, total_weight = solver_2.a_star_search()
        pass
    else:
        return

    if path:
        print("---------------------------------------------")
        step_size = len(path)
        file_path = create_file_path()
        to_output_file(file_path + '\output.txt', path, step_size, nodes,
                       total_weight, time, memory, algorithm, ID)
        print(f"Solution found! Step: {step_size} Nodes expanded: {
              nodes}, Total weight: {total_weight}")
        print(path)
        player_path = list(path.upper())
        game = Game(maze, player_path, stone_weight)
        game.run()
        print("---------------------------------------------")
    else:
        game = Game(maze, [], stone_weight)
        game.run()
        step_size = 0
        file_path = create_file_path()
        to_output_file(file_path + '\output.txt', path, step_size, nodes,
                       total_weight, time, memory, algorithm, ID)
        print("---------------------------------------------")
        print("Result: No solution found")
        print("---------------------------------------------")
