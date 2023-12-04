# In server.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class FileExchangeServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

        self.clients = {}
        self.files = {}

        # Tkinter GUI setup
        self.root = tk.Tk()
        self.root.title("File Exchange Server")
        self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=20)
        self.output_text.pack(padx=10, pady=10)

    def start_server(self):
        print("Server is running...")
        threading.Thread(target=self.accept_connections).start()
        self.root.mainloop()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            handle = client_socket.recv(1024).decode("utf-8")
            self.clients[handle] = client_socket
            self.display_output(f"User {handle} connected.")

            while True:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break
                self.process_command(handle, data)

        except Exception as e:
            print(f"Error: {e}")

    def process_command(self, handle, command):
        parts = command.split(" ", 1)
        command_name = parts[0].lower()

        if command_name == "/store":
            self.handle_store_command(handle, parts[1])
        elif command_name == "/dir":
            self.handle_dir_command(handle)
        elif command_name == "/get":
            self.handle_get_command(handle, parts[1])
        else:
            self.broadcast_message(handle, f"Error: Command not found: {command}")

    def handle_store_command(self, handle, filename):
        if handle not in self.files:
            self.files[handle] = []
        self.files[handle].append(filename)
        self.broadcast_message(handle, f"{handle} is storing file: {filename}")

    def handle_dir_command(self, handle):
        if handle in self.files:
            file_list = "\n".join(self.files[handle])
            self.send_message(handle, f"Server Directory\n{file_list}")
        else:
            self.send_message(handle, "Server Directory: No files available")

    def handle_get_command(self, handle, filename):
        if handle in self.files and filename in self.files[handle]:
            self.send_message(handle, f"File received from Server: {filename}")
        else:
            self.send_message(handle, f"Error: File not found in the server: {filename}")

    def broadcast_message(self, sender_handle, message):
        for h, client_socket in self.clients.items():
            if h != sender_handle:
                try:
                    client_socket.send(f"{sender_handle}: {message}".encode("utf-8"))
                except Exception as e:
                    print(f"Error: {e}")

    def send_message(self, handle, message):
        if handle in self.clients:
            client_socket = self.clients[handle]
            try:
                client_socket.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error: {e}")

    def display_output(self, message):
        print(message)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

if __name__ == "__main__":
    server = FileExchangeServer("127.0.0.1", 12345)
    server.start_server()