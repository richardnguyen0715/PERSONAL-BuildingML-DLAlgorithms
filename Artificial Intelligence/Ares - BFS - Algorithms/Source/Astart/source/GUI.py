import pygame
import time
import os
from pathlib import Path

# Game constants
TILE_SIZE = 40
Statistic_height = 100

class Game:
    def __init__(self, maze, player_path,stone_weights):
        pygame.init()
        self.original_maze = maze
        self.original_path = player_path
        self.stone_weights=stone_weights
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.step =0
        self.weight_being_pushed = 0

        # Calculate window dimensions with space for buttons
        self.button_height = 40
        self.screen_width = max(1000, self.cols * TILE_SIZE)
        self.screen_height = self.rows * TILE_SIZE + self.button_height + Statistic_height
        self.statistic_position = [(10,self.rows * TILE_SIZE),(500,self.rows * TILE_SIZE)]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("A* search algorithm")

        # Button properties
        self.restart_button_rect = pygame.Rect(
            self.screen_width // 2 - 50,  # x position
            self.rows * TILE_SIZE + 5 + Statistic_height,  # y position
            100,  # width
            30  # height
        )

        self.start_button_rect = pygame.Rect(
            self.screen_width // 2 - 250,  # x position
            self.rows * TILE_SIZE + 5 + Statistic_height,  # y position
            100,  # width
            30  # height
        )

        self.pause_button_rect = pygame.Rect(
            self.screen_width // 2 + 150,  # x position
            self.rows * TILE_SIZE + 5 + Statistic_height,  # y position
            100,  # width
            30  # height
        )

        # Initialize fonts
        self.font = pygame.font.Font(None, 36)

        # Load images
        self.load_game_images()

        self.reset_game()

    def draw_text(self, text, position):
        # Tạo văn bản
        text_surface = self.font.render(text, True,  (0, 0, 0))
        self.screen.blit(text_surface, position)  # Vẽ văn bản lên màn hình
    def load_game_images(self):
        current_directory = Path.cwd()
        parent_directory = current_directory.parent
        """Load all game images"""
        # Kết hợp đường dẫn tới file ảnh
        image_path = parent_directory / "assets" / "player.png"
        self.player_img = pygame.image.load(str(image_path))
        image_path = parent_directory / "assets" / "stone.png"
        self.stone_img = pygame.image.load(str(image_path))
        image_path = parent_directory / "assets" / "wall.png"
        self.wall_img = pygame.image.load(str(image_path))

        # Scale images to tile size
        self.player_img = pygame.transform.scale(self.player_img, (TILE_SIZE, TILE_SIZE))
        self.stone_img = pygame.transform.scale(self.stone_img, (TILE_SIZE, TILE_SIZE))
        self.wall_img = pygame.transform.scale(self.wall_img, (TILE_SIZE, TILE_SIZE))

    def reset_game(self):
        """Reset the game to initial state"""
        self.maze = [list(row) for row in self.original_maze]
        self.player_path = self.original_path
        self.current_path_index = 0
        self.load_positions()
        self.game_paused = False
        self.game_started = False  # Track game start state

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

    def draw_buttons(self):
        # Draw restart button
        button_color = (100, 100, 255)
        pygame.draw.rect(self.screen, button_color, self.restart_button_rect)
        text = self.font.render("Restart", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(text, text_rect)

        # Draw start button
        button_color = (0, 255, 0)
        pygame.draw.rect(self.screen, button_color, self.start_button_rect)
        text = self.font.render("Start", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(text, text_rect)

        # Draw pause button
        button_color = (255, 165, 0)
        pygame.draw.rect(self.screen, button_color, self.pause_button_rect)
        text = self.font.render("Pause", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.pause_button_rect.center)
        self.screen.blit(text, text_rect)

    def draw(self):
        # Draw background
        self.screen.fill((255, 255, 255))

        # Draw maze walls using wall image
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == '#':
                    self.screen.blit(self.wall_img, (j * TILE_SIZE, i * TILE_SIZE))

        # Draw targets (red circles)
        for target in self.targets:
            circle_center = (
                target[1] * TILE_SIZE + TILE_SIZE // 2,  # x coordinate
                target[0] * TILE_SIZE + TILE_SIZE // 2  # y coordinate
            )
            circle_radius = TILE_SIZE // 4  # Size of the circle
            pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius)

        # Draw stones using stone image
        for index, stone in enumerate(self.stones):
            # Vẽ viên đá
            self.screen.blit(self.stone_img,
                             (stone[1] * TILE_SIZE, stone[0] * TILE_SIZE))

            # Lấy stone_weight tương ứng
            stone_weight = self.stone_weights[index]

            # Vẽ stone_weight lên viên đá
            weight_text = str(stone_weight)  # Chuyển stone_weight thành chuỗi
            # Lấy kích thước của văn bản
            text_surface = self.font.render(weight_text, True, (255, 255, 255))  # Thay đổi màu sắc nếu cần
            text_width, text_height = text_surface.get_size()

            # Tính toán vị trí vẽ văn bản sao cho căn giữa
            text_position = (
                stone[1] * TILE_SIZE + (TILE_SIZE - text_width) // 2,  # Căn giữa theo trục x
                stone[0] * TILE_SIZE + (TILE_SIZE - text_height) // 2  # Căn giữa theo trục y
            )

            self.screen.blit(text_surface, text_position)  # Vẽ văn bản lên màn hình

            # Gọi phương thức vẽ văn bản
            self.draw_text(weight_text, text_position)

        # Draw player using player image
        self.screen.blit(self.player_img,
                         (self.player_pos[1] * TILE_SIZE,
                          self.player_pos[0] * TILE_SIZE))

        # Draw buttons
        self.draw_buttons()
        self.drawTextBox()
        pygame.display.flip()

    # def drawTextBox(self):

    def drawTextBox(self):
        # Vẽ Step
        step_text = f"The step count: {self.current_path_index}"
        step_surface = self.font.render(step_text, True, (0, 0, 0))
        self.screen.blit(step_surface, self.statistic_position[0])  # Vị trí góc trên bên trái

        # Vẽ Weight being pushed
        weight_text = f"The weight being pushed: {self.weight_being_pushed}"
        weight_surface = self.font.render(weight_text, True, (0, 0, 0))
        self.screen.blit(weight_surface, self.statistic_position[1])  # Vị trí ngay bên dưới Step
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.restart_button_rect.collidepoint(pos):
            self.reset_game()
            return True
        elif self.start_button_rect.collidepoint(pos):
            if not self.game_started:
                self.game_started = True  # Start the game
            return True
        elif self.pause_button_rect.collidepoint(pos):
            self.game_paused = not self.game_paused  # Toggle pause
            return True
        return False

    def move_player(self, direction):
        dx, dy = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[direction]
        new_Ares_pos = [self.player_pos[0] + dx, self.player_pos[1] + dy]

        # Check for stone
        stone_idx = None
        for i, stone in enumerate(self.stones):
            if stone[0] == new_Ares_pos[0] and stone[1] == new_Ares_pos[1]:
                stone_idx = i
                break

        if stone_idx is not None:
            # Calculate new stone position
            new_stone_pos = [new_Ares_pos[0] + dx, new_Ares_pos[1] + dy]

            # Check if stone can be pushed
            if (self.maze[new_stone_pos[0]][new_stone_pos[1]] != '#' and
                    not any(s[0] == new_stone_pos[0] and s[1] == new_stone_pos[1]
                            for s in self.stones)):
                # Move stone
                self.stones[stone_idx] = new_stone_pos
                # Move player
                self.player_pos = new_Ares_pos
                self.weight_being_pushed+=self.stone_weights[stone_idx]
                return True
        else: #Không có đá tại vị trí mới
            # Move player if no wall
            if self.maze[new_Ares_pos[0]][new_Ares_pos[1]] != '#':
                self.player_pos = new_Ares_pos
                return True
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.handle_click(event.pos):
                            continue

            if self.game_started and not self.game_paused and self.current_path_index < len(self.player_path):
                # Get next move from path
                direction = self.player_path[self.current_path_index]
                if self.move_player(direction):
                    self.current_path_index += 1
                    self.step +=1

                    # Check win condition
                    if all((stone[0], stone[1]) in self.targets for stone in self.stones):
                        self.game_paused = True

            self.draw()
            clock.tick(4)  # Control animation speed

        pygame.quit()


