import socket
import threading
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print("Server is waiting for connections...")

clients = []
ready_players = set()
users_connected = 0

def handle_client(client):
    global ready_players
    global users_connected

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'CONN':
                users_connected += 1
            elif message == 'READY':
                ready_players.add(client)
                if len(ready_players) == 2:
                    for c in clients:
                        c.send('START'.encode('utf-8'))
            elif message == 'EXIT':
                break
            else:
                # Broadcast the move to other player
                for other_client in clients:
                    if other_client != client:
                        other_client.send(message.encode('utf-8'))
                        check_game_state()
        except:
            break

    client.close()
    clients.remove(client)

def check_game_state():
    global ready_players
    global users_connected

    if len(ready_players) == 2 and users_connected == 2:
        # Add your game logic here
        print("Game logic goes here...")

# Accept connections
while users_connected < 2:
    client, addr = server_socket.accept()
    print(f"Connection from {addr} accepted.")
    clients.append(client)

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()

# The game logic will now run in the check_game_state function, called after each move.
