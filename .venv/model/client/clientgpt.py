import socket
import threading
import os
from datetime import datetime

class FileExchangeClient:
    def __init__(self):
        self.server_ip = ""
        self.server_port = 0
        self.handle = ""
        self.socket = None

    def connect_to_server(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.server_ip, self.server_port))
            threading.Thread(target=self.receive_messages).start()
            self.print_server_message("Connection to the File Exchange Server is successful!")
        except Exception as e:
            self.print_error_message(f"Error: Connection to the Server has failed! {str(e)}")

    def disconnect_from_server(self):
        if self.socket:
            self.socket.close()
            self.print_server_message("Connection closed. Thank you!")
        else:
            self.print_error_message("Error: Disconnection failed. Please connect to the server first.")

    def register_handle(self, handle):
        self.handle = handle
        self.print_server_message(f"Welcome {handle}!")

    def send_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                data = file.read()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"{self.handle}<{timestamp}>: Uploaded {filename}"
                self.print_server_message(message)
                # Implement file sending logic here
                # For simplicity, let's assume you send the file data as a message
                self.socket.sendall(data)
        else:
            self.print_error_message("Error: File not found.")

    def request_directory_list(self):
        # Implement directory list request logic
        try:
            self.socket.sendall(b'list')
        except Exception as e:
            self.print_error_message(f"Error: {str(e)}")
        

    def fetch_file(self, filename):
        # Implement file fetching logic
        try:
            self.socket.sendall(b'fetch')
        except Exception as e:
            self.print_error_message(f"Error: {str(e)}")

    def print_server_message(self, message):
        print(message)

    def print_error_message(self, error_message):
        print(error_message)

    def process_user_input(self, user_input):
        parts = user_input.split(' ')
        command = parts[0].lower()
        if command == '/join':
            self.connect_to_server(parts[1], int(parts[2]))
        elif command == '/leave':
            self.disconnect_from_server()
        elif command == '/register':
            self.register_handle(parts[1])
        elif command == '/store':
            self.send_file(parts[1])
        # Add more commands as needed

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.print_server_message(message)
            except Exception as e:
                print(f"Error: {str(e)}")
                break

    def start(self):
        while True:
            user_input = input("Enter a command: ")
            if user_input.lower() == '/quit':
                break
            self.process_user_input(user_input)

# Instantiate the client and start
client = FileExchangeClient()
client.start()