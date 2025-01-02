import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOVER_COLOR = (200, 200, 200)  # Color when hovered
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
GRID_SIZE = 3

# Font for text
font = pygame.font.SysFont("comicsans", 40)
small_font = pygame.font.SysFont("comicsans", 30)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Difficulty levels
difficulty = "easy"
difficulty_options = ["easy", "normal", "hard"]
selected_option = 0  # Index to keep track of the selected difficulty

# Functions to draw lines and figures
def draw_lines():
    pygame.draw.line(screen, BLACK, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2 * HEIGHT / 3), (WIDTH, 2 * HEIGHT / 3), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * WIDTH / 3, 0), (2 * WIDTH / 3, HEIGHT), LINE_WIDTH)

def draw_figures(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * WIDTH // 3 + SPACE, row * HEIGHT // 3 + SPACE), 
                                 ((col + 1) * WIDTH // 3 - SPACE, (row + 1) * HEIGHT // 3 - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (col * WIDTH // 3 + SPACE, (row + 1) * HEIGHT // 3 - SPACE),
                                 ((col + 1) * WIDTH // 3 - SPACE, row * HEIGHT // 3 + SPACE), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE, (col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_win(board, player):
    for row in range(3):
        if board[row] == [player, player, player]:
            return True
    for col in range(3):
        if [board[row][col] for row in range(3)] == [player, player, player]:
            return True
    if [board[i][i] for i in range(3)] == [player, player, player]:
        return True
    if [board[i][2 - i] for i in range(3)] == [player, player, player]:
        return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def reset_game():
    return [[" " for _ in range(3)] for _ in range(3)]

# AI logic for different difficulties
def ai_move(board, difficulty):
    available_moves = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == " "]
    if difficulty == 'easy':
        return random.choice(available_moves)
    elif difficulty == 'normal':
        return random.choice(available_moves)
    elif difficulty == 'hard':
        return random.choice(available_moves)  # Here you can add Min-Max logic for harder AI

# Start screen logic
def start_screen():
    global difficulty
    screen.fill(WHITE)
    title_text = font.render("Tic-Tac-Toe Game", True, BLACK)
    instruction_text = font.render("Press Space to Start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                select_difficulty()

# Difficulty selection screen with hover effect
def select_difficulty():
    global difficulty, selected_option
    screen.fill(WHITE)
    title_text = font.render("Select Difficulty", True, BLACK)

    easy_text = small_font.render("Easy", True, BLACK)
    normal_text = small_font.render("Normal", True, BLACK)
    hard_text = small_font.render("Hard", True, BLACK)
    
    # Detect mouse position for hover effect
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check if mouse is over the text and change color
    easy_color = HOVER_COLOR if (WIDTH // 2 - easy_text.get_width() // 2 < mouse_x < WIDTH // 2 + easy_text.get_width() // 2) and (HEIGHT // 2 - 60 < mouse_y < HEIGHT // 2 - 30) else BLACK
    normal_color = HOVER_COLOR if (WIDTH // 2 - normal_text.get_width() // 2 < mouse_x < WIDTH // 2 + normal_text.get_width() // 2) and (HEIGHT // 2 < mouse_y < HEIGHT // 2 + 30) else BLACK
    hard_color = HOVER_COLOR if (WIDTH // 2 - hard_text.get_width() // 2 < mouse_x < WIDTH // 2 + hard_text.get_width() // 2) and (HEIGHT // 2 + 60 < mouse_y < HEIGHT // 2 + 90) else BLACK

    # Render the texts with the appropriate color based on hover effect
    easy_text = small_font.render("Easy", True, easy_color)
    normal_text = small_font.render("Normal", True, normal_color)
    hard_text = small_font.render("Hard", True, hard_color)
    
    # Display difficulty options
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(normal_text, (WIDTH // 2 - normal_text.get_width() // 2, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 60))
    
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_color == HOVER_COLOR:
                    difficulty = "easy"
                elif normal_color == HOVER_COLOR:
                    difficulty = "normal"
                elif hard_color == HOVER_COLOR:
                    difficulty = "hard"
                waiting = False
                game_loop()

# Try Again screen
def try_again_screen(result, rounds):
    screen.fill(WHITE)
    message = font.render(f"{result} in {rounds} turns!", True, BLACK)
    instruction_text = font.render("Press Space to Try Again", True, BLACK)
    
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                game_loop()

# Main game loop
def game_loop():
    board = reset_game()
    current_player = "X"
    game_over = False
    rounds = 0

    while True:
        screen.fill(WHITE)
        draw_lines()
        draw_figures(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // (WIDTH // 3)
                mouseY = event.pos[1] // (HEIGHT // 3)
                if board[mouseY][mouseX] == " ":
                    board[mouseY][mouseX] = current_player
                    rounds += 1
                    if check_win(board, current_player):
                        game_over = True
                        try_again_screen(f"Player {current_player} Wins", rounds)
                    elif check_draw(board):
                        game_over = True
                        try_again_screen("It's a Draw!", rounds)
                    current_player = "O" if current_player == "X" else "X"

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_loop()

        if not game_over and current_player == "O":
            ai_row, ai_col = ai_move(board, difficulty)
            board[ai_row][ai_col] = "O"
            rounds += 1
            if check_win(board, "O"):
                game_over = True
                try_again_screen(f"AI Wins", rounds)
            elif check_draw(board):
                game_over = True
                try_again_screen("It's a Draw!", rounds)
            current_player = "X"
            
        pygame.display.update()

if __name__ == "__main__":
    start_screen()
