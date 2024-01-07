import socket
import threading

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'START':
                print("Game started! You are 'X'.")
                print_board()
            elif message.startswith('MOVE'):
                _, row, col, symbol = message.split(',')
                make_move(int(row), int(col), symbol)
                print_board()
            elif message == 'WIN':
                print("Congratulations! You won!")
                break
            elif message == 'DRAW':
                print("It's a draw!")
                break
        except:
            break

def make_move(row, col, symbol):
    board[row][col] = symbol

def print_board():
    for row in board:
        print(" ".join(row))
    print()

# Initialize the tic-tac-toe board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Send 'CONN' to server to indicate connection
client_socket.send('CONN'.encode('utf-8'))

# Wait for user input to start the game
input("Press Enter when ready to start the game...")

# Send 'READY' to server to indicate readiness
client_socket.send('READY'.encode('utf-8'))

# Your game initialization logic goes here

# For example, you can create a simple loop for the game
while True:
    try:
        move = input("Your move (row, col): ")
        if move.upper() == 'EXIT':
            client_socket.send(move.encode('utf-8'))
            break

        row, col = map(int, move.split(','))
        if board[row][col] == ' ':
            make_move(row, col, 'X')
            client_socket.send(f'MOVE,{row},{col},X'.encode('utf-8'))
        else:
            print("Invalid move. Cell already taken.")
    except (ValueError, IndexError):
        print("Invalid input. Please enter row and column as integers separated by a comma.")

# Close the connection when the game ends
client_socket.close()
