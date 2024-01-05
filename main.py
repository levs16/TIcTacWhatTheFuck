import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
GRID_SIZE = 3
SQUARE_SIZE = WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-What-The-Fuck")

# Board
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 'X'

# Result view variables
result_view = False
result_message = ""

# Logging variables
log = []

# Functions
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

def draw_markers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                                 (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, LINE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                        row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2, LINE_WIDTH)

def draw_text(text, x, y):
    text_surface = FONT.render(text, True, LINE_COLOR)
    screen.blit(text_surface, (x, y))

def check_winner():
    # Check rows, columns, and diagonals for a winner
    for i in range(GRID_SIZE):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]  # Winner in row
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]  # Winner in column
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]  # Winner in main diagonal
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]  # Winner in secondary diagonal
    return None

def is_board_full():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == '':
                return False
    return True

def reset_game():
    global board, current_player, result_view, result_message, log
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = 'X'
    result_view = False
    result_message = ""
    log = []

def log_move(move_type):
    global log
    log.append(f"{len(log) + 1}: {move_type}\n" + get_ascii_board())

def get_ascii_board():
    return "\n".join([" ".join(row) for row in board])

# Function to get the starting player choice
def get_starting_player():
    while True:
        choice = input("Choose the starting player (X or O): ").upper()
        if choice in ['X', 'O']:
            return choice
        else:
            print("Invalid choice. Please enter X or O.")

# Ask for the starting player at the beginning
starting_player = get_starting_player()
current_player = starting_player

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if not result_view:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == '' and not check_winner():
                    board[clicked_row][clicked_col] = current_player
                    log_move(f"{current_player} MOVE")
                    if current_player == 'X':
                        current_player = 'O'
                    else:
                        current_player = 'X'

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                if WIDTH // 2 - 60 <= mouseX <= WIDTH // 2 + 60 and HEIGHT // 2 + 20 <= mouseY <= HEIGHT // 2 + 60:
                    reset_game()

    screen.fill(WHITE)

    if not result_view:
        draw_grid()
        draw_markers()

        winner = check_winner()
        if winner:
            result_message = f"Player {winner} wins!"
            log_move(f"{winner} WINS")
        elif is_board_full():
            result_message = "It's a tie!"
            log_move("TIE")

        if winner or is_board_full():
            result_view = True
    else:
        draw_text(result_message, WIDTH // 2 - 120, HEIGHT // 2 - 50)
        pygame.draw.rect(screen, LINE_COLOR, (WIDTH // 2 - 60, HEIGHT // 2 + 20, 120, 40), 2)
        draw_text("Restart", WIDTH // 2 - 40, HEIGHT // 2 + 30)

    pygame.display.flip()

# Display the log after the game ends
for entry in log:
    print(entry)

# Quit Pygame
pygame.quit()
