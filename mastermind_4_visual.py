import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)

COLORS = {"red": RED, "blue": BLUE, "green": GREEN, "yellow": YELLOW}
COLOR_OPTIONS = list(COLORS.keys())

# Game settings
MAX_ATTEMPTS = 10
CIRCLE_RADIUS = 30
CIRCLE_SPACING = 100
CASE_WIDTH = 60
CASE_HEIGHT = 60

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mastermind Game")

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Game class
class MastermindGame:
    def __init__(self):
        self.secret_combination = []
        self.attempts = []
        self.max_attempts = MAX_ATTEMPTS
        self.current_guess = []
        self.feedback = []
        self.menu_active = True  # Whether we are in the menu
        self.game_won = False

    def setup_game(self):
        # Generate the secret combination with no repeated colors
        self.secret_combination = random.sample(COLOR_OPTIONS, 4)
        print(f"Secret combination: {self.secret_combination}")  # Debugging
        self.attempts = []
        self.feedback = []
        self.current_guess = []
        self.game_won = False

    def evaluate_guess(self):
        # Evaluate the player's guess
        guess = self.current_guess
        exact_matches = 0
        secret_copy = self.secret_combination.copy()

        # Exact matches
        for i in range(4):
            if guess[i] == secret_copy[i]:
                exact_matches += 1
                secret_copy[i] = None  # Remove this from being counted twice

        # Check if the player won
        if exact_matches == 4:
            self.game_won = True

        feedback = f"{exact_matches} exact matches."
        return feedback

    def draw_menu(self):
        screen.fill(BLACK)
        title_text = big_font.render("Mastermind Game", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

        start_text = font.render("Press SPACE to start the game", True, WHITE)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def draw_game(self):
        # Set the background to black
        screen.fill(BLACK)

        # Draw previous attempts and feedback on the right side
        x_text_start = SCREEN_WIDTH - 300
        for idx, (attempt, feedback) in enumerate(zip(self.attempts, self.feedback)):
            attempt_text = font.render(f"Attempt {idx + 1}: {feedback}", True, WHITE)
            screen.blit(attempt_text, (x_text_start, 50 + idx * 100))
            self.draw_guess(attempt, 50, 100 + idx * 100)

        # Draw the current guess
        self.draw_guess(self.current_guess, 50, SCREEN_HEIGHT - 150)

        # Draw "cases" for the current guess
        self.draw_cases(50, SCREEN_HEIGHT - 150)

        # Draw feedback for current guess if it exists
        if self.feedback:
            feedback_text = font.render(self.feedback[-1], True, WHITE)
            screen.blit(feedback_text, (x_text_start, SCREEN_HEIGHT - 150))

    def draw_guess(self, guess, x_start, y_pos):
        """Draw the colored circles representing a guess."""
        for i, color in enumerate(guess):
            pygame.draw.circle(screen, COLORS[color], (x_start + i * CIRCLE_SPACING, y_pos), CIRCLE_RADIUS)

    def draw_cases(self, x_start, y_pos):
        """Draw empty cases (squares) where the guesses will be placed."""
        for i in range(4):
            pygame.draw.rect(screen, DARK_GRAY, 
                             (x_start + i * CIRCLE_SPACING - CASE_WIDTH // 2, 
                              y_pos - CASE_HEIGHT // 2, CASE_WIDTH, CASE_HEIGHT), 3)

    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.menu_active = False
            self.setup_game()

    def handle_game_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.current_guess.append("red")
            elif event.key == pygame.K_b:
                self.current_guess.append("blue")
            elif event.key == pygame.K_g:
                self.current_guess.append("green")
            elif event.key == pygame.K_y:
                self.current_guess.append("yellow")
            
            # Submit guess when 4 colors are chosen
            if len(self.current_guess) == 4:
                self.attempts.append(self.current_guess.copy())
                feedback = self.evaluate_guess()
                self.feedback.append(feedback)
                self.current_guess = []  # Reset for the next guess

                # Check if the game is won or lost
                if self.game_won:
                    self.show_win_message()
                elif len(self.attempts) == self.max_attempts:
                    self.show_loss_message()

    def show_win_message(self):
        """Display a win message and return to the menu after a few seconds."""
        screen.fill(BLACK)
        win_text = big_font.render("Congratulations! You won!", True, WHITE)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        time.sleep(3)  # Pause for 3 seconds before returning to menu
        self.menu_active = True  # Return to menu

    def show_loss_message(self):
        """Display a game over message and return to the menu after a few seconds."""
        screen.fill(BLACK)
        loss_text = big_font.render("Game Over! You lost!", True, WHITE)
        correct_combination_text = font.render(f"The correct combination was: {', '.join(self.secret_combination)}", True, WHITE)
        screen.blit(loss_text, (SCREEN_WIDTH // 2 - loss_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(correct_combination_text, (SCREEN_WIDTH // 2 - correct_combination_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()
        time.sleep(3)  # Pause for 3 seconds before returning to menu
        self.menu_active = True  # Return to menu

# Main game loop
def main():
    game = MastermindGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game.menu_active:
                game.handle_menu_input(event)
            else:
                game.handle_game_input(event)

        if game.menu_active:
            game.draw_menu()
        else:
            game.draw_game()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
