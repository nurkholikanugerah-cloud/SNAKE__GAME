import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 20
FPS = 5  # Slower speed for realistic feel

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (39, 174, 96)
RED = (231, 76, 60)
DARK_BLUE = (26, 37, 47)
BACKGROUND = (44, 62, 80)
BUTTON_COLOR = (52, 73, 94)
BUTTON_HOVER = (66, 89, 112)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Extra space for UI
        pygame.display.set_caption("🐍 Realistic Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Load high score
        self.high_score = self.load_high_score()

        # Game state
        self.reset_game()

        # Load images (fallback to shapes if images fail)
        self.load_images()

    def load_images(self):
        try:
            # Try to load snake pattern (using a simple pattern instead of external URL)
            self.snake_pattern = pygame.Surface((GRID_SIZE, GRID_SIZE))
            self.snake_pattern.fill(GREEN)
            pygame.draw.circle(self.snake_pattern, (30, 150, 80), (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 2)

            # Create apple image
            self.apple_img = pygame.Surface((GRID_SIZE-4, GRID_SIZE-4))
            self.apple_img.fill(RED)
            pygame.draw.circle(self.apple_img, (200, 50, 50), ((GRID_SIZE-4)//2, (GRID_SIZE-4)//2), (GRID_SIZE-4)//2)
        except:
            self.snake_pattern = None
            self.apple_img = None

    def load_high_score(self):
        try:
            if os.path.exists('high_score.txt'):
                with open('high_score.txt', 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return 0

    def save_high_score(self):
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass

    def reset_game(self):
        self.snake = [(WIDTH//2//GRID_SIZE, HEIGHT//2//GRID_SIZE)]
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.score = 0
        self.game_running = False
        self.game_over = False
        self.generate_food()

    def generate_food(self):
        while True:
            self.food = (random.randint(0, (WIDTH//GRID_SIZE)-1),
                        random.randint(0, (HEIGHT//GRID_SIZE)-1))
            if self.food not in self.snake:
                break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if not self.game_running and not self.game_over:
                    self.game_running = True

                if event.key == pygame.K_LEFT and self.direction[0] == 0:
                    self.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction[0] == 0:
                    self.next_direction = (1, 0)
                elif event.key == pygame.K_UP and self.direction[1] == 0:
                    self.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction[1] == 0:
                    self.next_direction = (0, 1)
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    return False
        return True

    def update(self):
        if not self.game_running or self.game_over:
            return

        # Update direction
        self.direction = self.next_direction

        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= WIDTH//GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= HEIGHT//GRID_SIZE):
            self.game_over = True
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.generate_food()
        else:
            self.snake.pop()

    def draw(self):
        # Clear screen
        self.screen.fill(BACKGROUND)

        # Draw game area background
        pygame.draw.rect(self.screen, DARK_BLUE, (0, 0, WIDTH, HEIGHT))

        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE

            if i == 0:  # Head
                # Draw snake head
                pygame.draw.circle(self.screen, GREEN,
                                 (x + GRID_SIZE//2, y + GRID_SIZE//2),
                                 GRID_SIZE//2 - 2)

                # Draw eyes based on direction
                eye_offset_x, eye_offset_y = 0, 0
                if self.direction[0] == 1: eye_offset_x = 5      # right
                elif self.direction[0] == -1: eye_offset_x = -5   # left
                elif self.direction[1] == -1: eye_offset_y = -5   # up
                elif self.direction[1] == 1: eye_offset_y = 5     # down

                # White part of eyes
                pygame.draw.circle(self.screen, WHITE,
                                 (x + GRID_SIZE//2 + eye_offset_x - 3, y + GRID_SIZE//2 + eye_offset_y - 3), 3)
                pygame.draw.circle(self.screen, WHITE,
                                 (x + GRID_SIZE//2 + eye_offset_x + 3, y + GRID_SIZE//2 + eye_offset_y - 3), 3)

                # Black pupils
                pygame.draw.circle(self.screen, BLACK,
                                 (x + GRID_SIZE//2 + eye_offset_x - 3, y + GRID_SIZE//2 + eye_offset_y - 3), 1)
                pygame.draw.circle(self.screen, BLACK,
                                 (x + GRID_SIZE//2 + eye_offset_x + 3, y + GRID_SIZE//2 + eye_offset_y - 3), 1)
            else:  # Body
                # Draw snake body segments
                pygame.draw.circle(self.screen, GREEN,
                                 (x + GRID_SIZE//2, y + GRID_SIZE//2),
                                 GRID_SIZE//2 - 2)

        # Draw food (apple)
        food_x, food_y = self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE
        pygame.draw.circle(self.screen, RED,
                         (food_x + GRID_SIZE//2, food_y + GRID_SIZE//2),
                         GRID_SIZE//2 - 2)

        # Draw UI
        self.draw_ui()

        # Draw game over screen
        if self.game_over:
            self.draw_game_over()

    def draw_ui(self):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)

        self.screen.blit(score_text, (20, HEIGHT + 20))
        self.screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, HEIGHT + 20))

        # Draw controls info
        controls_text = self.small_font.render("Arrow Keys: Move | R: Restart | Q: Quit", True, WHITE)
        self.screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT + 60))

    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT + 100))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Game over text
        game_over_text = self.font.render("Game Over!", True, RED)
        final_score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.small_font.render("Press R to restart or Q to quit", True, WHITE)

        self.screen.blit(game_over_text,
                        (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        self.screen.blit(final_score_text,
                        (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
        self.screen.blit(restart_text,
                        (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()

            if self.game_over and self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
