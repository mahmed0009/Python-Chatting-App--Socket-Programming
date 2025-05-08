import socket
import threading

clients = []


def handle_client(client_socket, addr):
    username = client_socket.recv(1024).decode('utf-8')
    clients.append((client_socket, username))
    print(f"[NEW CONNECTION]{username} connected from {addr}")
    
    broadcast(f"{username} joined the chat!", client_socket)

    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                full_msg = f"{username}: {msg}"
                print(full_msg)
                broadcast(full_msg, client_socket)
            else:
                break
        except:
            break

    clients.remove((client_socket, username))
    client_socket.close()
    broadcast(f"{username} left the chat!", client_socket)


def broadcast(msg, sender_socket):
    for client_socket, _ in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(msg.encode('utf-8'))
            except:
                clients.remove((client_socket, _))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen()
    print("[SERVER STARTED]  Server is listening...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()


start_server()       