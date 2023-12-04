# In client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog  # Added simpledialog

class Client:
    # def __init__(self):
    #     # Tkinter GUI setup
    #     self.root = tk.Tk()
    #     self.root.title("File Exchange Client")
    #     self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=20)
    #     self.output_text.pack(padx=10, pady=10)
    #     self.input_entry = Entry(self.root, width=30)
    #     self.input_entry.pack(pady=5)
    #     self.send_button = Button(self.root, text="Send", command=None)
    #     self.send_button.pack(pady=5)

    #     self.server_host = None
    #     self.server_port = None
    #     self.socket = None
    #     self.commands = {
    #         "/join": {
    #             "desc": "Connect to the server application",
    #             "usage": "/join <server_ip_add> <port>",
    #             "call": self.connect
    #         }, 
    #         "/leave": {
    #             "desc": "Disconnect from the server application",
    #             "usage": "/leave",
    #             "call": self.disconnect
    #         }, 
    #         "/register": {
    #             "desc": "Register a unique handle or alias",
    #             "usage": "/register <handle>",
    #             "call": None
    #         },
    #         "/store":{
    #             "desc": "Send file to server",
    #             "usage": "/store <filename>",
    #             "call": None
    #         }, 
    #         "/dir": {
    #             "desc": "Request directory file list from a server",
    #             "usage": "/dir",
    #             "call": None
    #         }, 
    #         "/get":{
    #             "desc": "Fetch a file from a server",
    #             "usage": "/get <filename>",
    #             "call": None
    #         },
    #         "/?":{
    #             "desc": "List of commands", 
    #             "usage": "/?",
    #             "call": self.commands
    #         }
    #     }

    # # GUI
    # def send_user_input(self):
    #     user_input = self.input_entry.get()
    #     self.process_user_input(user_input)

    # def start_console(self, command):
    #     try:
    #         isValid, args = self.check_command(command)
    #         if isValid: 
    #             return self.commands[args[0]]["call"](args)
    #         else: 
    #             raise Exception("Command not found.")
            
    #     except Exception as e:
    #         errorMsg = f"Error: {e}"
    #         print(errorMsg)
    #         return errorMsg

    # def check_command(self, params):
    #     if len(params) == 0:
    #         return False, None
    #     else:
    #         args = params.split(" ")
    #         if isinstance(args, str):
    #             args = [args]

    #         if args[0] in self.commands.keys():
    #             return True, args
    #         else:
    #             return False, None

    # def connect(self, params):
    #     try:
    #         if len(params) != 3 or not params[2].isdigit(): 
    #             raise Exception("Command parameters do not match or is not allowed.")
    #         # elif self.socket is not None:
    #         #     raise Exception("Connection to the Server is already established.")
    #         self.server_host = params[1]
    #         self.server_port = int(params[2])
    #         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    #         self.socket.connect((self.server_host, self.server_port))
    #         msg = "Connection to the File Exchange Server is successful!"
    #         print(msg)
    #         return msg
    #     except ConnectionError as ce:
    #         self.socket = None
    #         msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
    #         print(msg)
    #         return msg
    #     except Exception as e:
    #         errorMsg = f"Error: {e}"
    #         print(errorMsg)
    #         return errorMsg

    # def disconnect(self, params):
    #     try:
    #         if self.socket is None:
    #             raise Exception("Disconnection failed. Please connect to the server first.")
    #         self.socket.close()
    #         self.socket = None
    #         msg = "Connection closed. Thank you!"
    #         print(msg)
    #         return msg
    #     except Exception as e:
    #         errorMsg = f"Error: {e}"
    #         print(f"Error: {e}")
    #         return errorMsg

    # def send_user_input(self, params): pass

    # def commands(self, params):
    #     print('-' * 20)
    #     print("List of commands")
    #     msg = []
    #     for command in self.commands: 
    #         print(self.commands[command]['desc'])
    #         print(self.commands[command]['usage'])
    #         msg.append(command + "\n - " + self.commands[command]['desc'] + "\n - " + self.commands[command]['usage'])
    #     print('-' * 20)
    #     return 

    def __init__(self):
        self.handle = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = None
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

    # sends user input to the server
    def send_user_input(self):
        command = self.input_entry.get()
        # self.output_text.insert(tk.END, f"User Input: {command}\n")
        try:
            isValid, args = self.check_command(command)
            if isValid: 
                res = self.commands[args[0]]["call"](args)
                self.output_text.insert(tk.END, f"{res}\n")
            else: 
                raise Exception("Command not found.")
            
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            self.output_text.insert(tk.END, f"{errorMsg}\n")

    # checks if the command is valid
    def check_command(self, params):
        if len(params) == 0:
            return False, None
        else:
            args = params.split(" ")
            if isinstance(args, str):
                args = [args]

            if args[0] in self.commands.keys():
                return True, args
            else:
                return False, None
    
    def connect_to_server(self, params):
        try:
            if len(params) != 3 or not params[2].isdigit(): 
                raise Exception("Command parameters do not match or is not allowed.")
            elif self.socket is not None:
                raise Exception("Connection to the Server is already established.")
            server_host = params[1]
            server_port = int(params[2])
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            self.socket.connect((server_host, server_port))
            msg = "Connection to the File Exchange Server is successful!"
            print(msg)
            return msg
        except ConnectionError as ce:
            self.socket = None
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def disconnect_from_server(self, params):
        try:
            if self.socket is None:
                raise Exception("Disconnection failed. Please connect to the server first.")
            self.socket.send('/leave ')
            self.socket.close()
            self.socket = None
            msg = "Connection closed. Thank you!"
            print(msg)
            return msg
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

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

    def send_file(self, filename):
        # Logic for sending a file to the server
        self.send_file_to_server(filename)

    def fetch_file(self, filename):
        # Logic for fetching a file from the server
        self.fetch_file_from_server(filename)

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
    client = Client()
    client.root.mainloop()
# client = Client()
# client.start_console()