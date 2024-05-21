import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                self.outout.append(message)
            else:
                break
        except:
            break

def start_client(server_ip, server_port, nickname):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message == '/quit':
            client_socket.send(f"{nickname} has left the chat.".encode('utf-8'))
            break
        else:
            client_socket.send(f"{nickname}: {message}".encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    start_client("127.0.0.1", 6667, nickname)
