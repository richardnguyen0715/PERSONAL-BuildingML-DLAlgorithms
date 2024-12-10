from Libraries import *
from Other_funcs import *
from BFS_Source import *
from ui import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
PADDING = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
ORANGE = (255, 140, 0)
PURPLE = (147, 112, 219)
HOVER_TINT = (20, 20, 20)
LIGHT_GREY = (211, 211, 211)

# Button class for reusability


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.original_color = color
        self.is_hovered = False

    def draw(self, surface: pygame.Surface):
        color = tuple(max(0, min(255, c - 30))
                      for c in self.color) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class AlgorithmMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Algorithm Selection")
        self.clock = pygame.time.Clock()
        self.selected_algorithm = None

        # Create algorithm buttons
        button_y = 100
        self.buttons = [
            Button(WINDOW_WIDTH//2 - BUTTON_WIDTH//2, button_y,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "BFS", BLUE),
            Button(WINDOW_WIDTH//2 - BUTTON_WIDTH//2, button_y + 80,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "DFS", GREEN),
            Button(WINDOW_WIDTH//2 - BUTTON_WIDTH//2, button_y + 160,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "UCS", ORANGE),
            Button(WINDOW_WIDTH//2 - BUTTON_WIDTH//2, button_y + 240,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "A*", PURPLE),
            Button(WINDOW_WIDTH//2 - BUTTON_WIDTH//2, button_y + 320,
                   BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", RED)
        ]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for i, button in enumerate(self.buttons):
                    if button.handle_event(event):
                        if i == len(self.buttons) - 1:  # Exit button
                            pygame.quit()
                            sys.exit()
                        else:
                            self.selected_algorithm = button.text
                            difficulty_menu = DifficultyMenu(
                                self.selected_algorithm)
                            difficulty_menu.run()

            self.screen.fill(WHITE)

            # Draw title
            font = pygame.font.Font(None, 48)
            title = font.render("Select Algorithm", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(title, title_rect)

            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)


ID = 0


class DifficultyMenu:
    def __init__(self, algorithm: str):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(f"{algorithm} - Difficulty Selection")
        self.clock = pygame.time.Clock()
        self.algorithm = algorithm

        # Create difficulty buttons
        self.reset_buttons()

    def reset_buttons(self):
        self.buttons = []

        # Easy buttons (4)
        easy_y = 150
        for i in range(4):
            self.buttons.append(
                Button(WINDOW_WIDTH//4 - BUTTON_WIDTH//2,
                       easy_y + i * 70,
                       BUTTON_WIDTH, BUTTON_HEIGHT,
                       f"Easy {i+1}", GREEN)
            )

        # Medium buttons (3)
        medium_y = 150
        for i in range(3):
            self.buttons.append(
                Button(WINDOW_WIDTH//2 - BUTTON_WIDTH//2,
                       medium_y + i * 70,
                       BUTTON_WIDTH, BUTTON_HEIGHT,
                       f"Medium {i+1}", ORANGE)
            )

        # Hard buttons (3)
        hard_y = 150
        for i in range(3):
            self.buttons.append(
                Button(3*WINDOW_WIDTH//4 - BUTTON_WIDTH//2,
                       hard_y + i * 70,
                       BUTTON_WIDTH, BUTTON_HEIGHT,
                       f"Hard {i+1}", RED)
            )

        # Back button
        self.back_button = Button(20, WINDOW_HEIGHT - 70,
                                  BUTTON_WIDTH, BUTTON_HEIGHT,
                                  "Back", PURPLE)

    def game(self, difficulty: str):
        global ID
        # Placeholder for the game function
        filepath = create_file_path()
        if difficulty == 'Easy 1':
            filepath = filepath + r'\Input\input_01.txt'
        elif difficulty == 'Easy 2':
            filepath = filepath + r'\Input\input_02.txt'
        elif difficulty == 'Easy 3':
            filepath = filepath + r'\Input\input_03.txt'
        elif difficulty == 'Easy 4':
            filepath = filepath + r'\Input\input_04.txt'
        elif difficulty == 'Medium 1':
            filepath = filepath + r'\Input\input_05.txt'
        elif difficulty == 'Medium 2':
            filepath = filepath + r'\Input\input_06.txt'
        elif difficulty == 'Medium 3':
            filepath = filepath + r'\Input\input_07.txt'
        elif difficulty == 'Hard 1':
            filepath = filepath + r'\Input\input_08.txt'
        elif difficulty == 'Hard 2':
            filepath = filepath + r'\Input\input_09.txt'
        elif difficulty == 'Hard 3':
            filepath = filepath + r'\Input\input_10.txt'

        open_maze_solver(filepath, self.algorithm, ID)
        ID += 1

    def run(self):
        # Set the display window size once when starting the difficulty selection screen
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.back_button.handle_event(event):
                    return

                for button in self.buttons:
                    if button.handle_event(event):
                        self.game(button.text)
                        # Reset the display mode after returning from the game
                        self.screen = pygame.display.set_mode(
                            (WINDOW_WIDTH, WINDOW_HEIGHT))

            self.screen.fill(WHITE)

            # Draw titles
            font = pygame.font.Font(None, 48)
            title = font.render(
                f"{self.algorithm} - Select Difficulty", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(title, title_rect)

            # Draw section titles
            font = pygame.font.Font(None, 36)
            sections = ["Easy", "Medium", "Hard"]
            for i, section in enumerate(sections):
                text = font.render(section, True, BLACK)
                text_rect = text.get_rect(
                    center=((i + 1) * WINDOW_WIDTH//4, 100))
                self.screen.blit(text, text_rect)

            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)

            self.back_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
