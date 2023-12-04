# In client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog  # Added simpledialog

class FileExchangeClient:
    def __init__(self, handle):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handle = handle

        # Define commands
        self.commands = {
            "/join": {
                "desc": "Connect to the server application",
                "usage": "/join",
                "call": self.connect_to_server
            },
            "/leave": {
                "desc": "Disconnect from the server application",
                "usage": "/leave",
                "call": self.disconnect_from_server
            },
            "/register": {
                "desc": "Register a unique handle or alias",
                "usage": "/register <handle>",
                "call": self.register_handle
            },
            "/store": {
                "desc": "Send file to server",
                "usage": "/store <filename>",
                "call": self.send_file_to_server
            },
            "/dir": {
                "desc": "Request directory file list from a server",
                "usage": "/dir",
                "call": self.request_directory_list
            },
            "/get": {
                "desc": "Fetch a file from a server",
                "usage": "/get <filename>",
                "call": self.fetch_file_from_server
            },
            "/?": {
                "desc": "List of commands",
                "usage": "/?",
                "call": self.show_commands
            }
        }

        # Tkinter GUI setup
        self.root = tk.Tk()
        self.root.title("File Exchange Client")
        self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=20)
        self.output_text.pack(padx=10, pady=10)
        self.input_entry = Entry(self.root, width=30)
        self.input_entry.pack(pady=5)
        self.send_button = Button(self.root, text="Send", command=self.send_user_input)
        self.send_button.pack(pady=5)

    def connect_to_server(self, server_ip, port):
        self.server_socket.connect((server_ip, port))
        self.server_socket.send(self.handle.encode("utf-8"))
        threading.Thread(target=self.receive_messages).start()

    def disconnect_from_server(self):
        self.server_socket.close()
        self.display_output("Connection closed. Thank you!")

    def register_handle(self, handle):
        self.handle = handle
        self.display_output(f"Welcome {handle}!")

    def send_file_to_server(self, filename):
        # Implement file sending logic
        self.send_message(f"/store {filename}")

    def request_directory_list(self):
        # Implement directory list request logic
        self.send_message("/dir")

    def fetch_file_from_server(self, filename):
        # Implement file fetching logic
        self.send_message(f"/get {filename}")

    def show_commands(self):
        for command, details in self.commands.items():
            self.display_output(f"{command}: {details['desc']} (Usage: {details['usage']})")

    def process_user_input(self, user_input):
        parts = user_input.split(" ", 1)
        command = parts[0].lower()

        if command in self.commands:
            if len(parts) > 1:
                arguments = parts[1]
            else:
                arguments = ""
            self.commands[command]["call"](arguments)
        else:
            self.display_output("Error: Command not found.")

    def send_file(self, filename):
        # Logic for sending a file to the server
        self.send_file_to_server(filename)

    def fetch_file(self, filename):
        # Logic for fetching a file from the server
        self.fetch_file_from_server(filename)

    def send_user_input(self):
        user_input = self.input_entry.get()
        self.process_user_input(user_input)

    def send_message(self, message):
        try:
            self.server_socket.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Error: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.server_socket.recv(1024).decode("utf-8")
                self.display_output(message)
            except Exception as e:
                break

    def display_output(self, message):
        print(message)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def show_join_dialog(self):
        server_ip = simpledialog.askstring("Server IP", "Enter Server IP Address:")
        server_port = simpledialog.askinteger("Server Port", "Enter Server Port:")
        return server_ip, server_port


if __name__ == "__main__":
    client = FileExchangeClient("Alice")
    client.root.mainloop()