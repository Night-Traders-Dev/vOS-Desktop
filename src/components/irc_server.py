import socket
import threading

clients = []

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                send(message, client_socket)
            else:
                clients.remove(client_socket)
                break
        except:
            clients.remove(client_socket)
            break

def start_server(server_ip, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server started on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server("127.0.0.1", 6667)
