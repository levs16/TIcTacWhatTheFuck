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

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Board
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 'X'

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

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] == '' and not check_winner():
                board[clicked_row][clicked_col] = current_player
                if current_player == 'X':
                    current_player = 'O'
                else:
                    current_player = 'X'

    screen.fill(WHITE)
    draw_grid()
    draw_markers()

    winner = check_winner()
    if winner:
        print(f"Player {winner} wins!")
        running = False

    if is_board_full() and not winner:
        print("It's a tie!")
        running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
