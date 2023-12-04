import socket
import threading
from datetime import datetime

class FileExchangeServer:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.server_port = 12345
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)

    def start_server(self):
        print(f"Server listening on {self.server_ip}:{self.server_port}")

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.broadcast_message(message, client_socket)
            except Exception as e:
                print(f"Error: {str(e)}")
                break

    def broadcast_message(self, message, sender):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} - {message}"
        print(formatted_message)
        for client in self.clients:
            if client != sender:
                try:
                    client.send(formatted_message.encode('utf-8'))
                except Exception as e:
                    print(f"Error: {str(e)}")
                    self.clients.remove(client)

    def handle_command(self, command, client_socket):
        # Implement handling client commands
        pass

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

# Instantiate the server and start
server = FileExchangeServer()
server.start_server()
server.run()