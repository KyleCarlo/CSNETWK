# In client.py
import socket
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog  # Added simpledialog
import os
import threading
class Client:
    def __init__(self):
        self.handle = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = None
        self.recv_message = True
        self.commands = {
            "/join": {
                "desc": "Connect to the server application",
                "usage": "/join <server_ip_add> <port>",
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
            "/clients": {
                "desc": "Get the list of clients connected to the server",
                "usage": "/getclients",
                "call": self.get_clients
            },
            "/msg": {
                "desc": "Message another client connected to the server",
                "usage": "/message <client_name> <message>",
                "call": self.message
            },
            "/msgall": {
                "desc": "Message clients connected to the server",
                "usage": "/msgall <message>",
                "call": self.message_all
            },
            "/?": {
                "desc": "List of commands",
                "usage": "/?",
                "call": self.show_commands
            }
        }

        # Tkinter GUI setup
        self.root = tk.Tk()
        self.root.title("Client File Exchange")
        self.output_text = scrolledtext.ScrolledText(self.root, width=100, height=20)
        self.output_text.pack(padx=10, pady=10)
        self.input_entry = Entry(self.root, width=30)
        self.input_entry.pack(pady=5)
        self.send_button = Button(self.root, text="Send", command=self.send_user_input)
        self.send_button.pack(pady=5)

    # sends user input to the server
    def send_user_input(self):
        
        command = self.input_entry.get()
        
        try:
            isValid, args = self.check_command(command)

            if isValid: 
                res = self.commands[args[0]]["call"](args)
                self.output_text.insert(tk.END, f"{res}\n")
                if 'Error:' not in res:
                    self.input_entry.delete(0, tk.END)
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
            if len(params) != 1: 
                raise Exception("Command parameters do not match or is not allowed.")
            elif self.socket is None:
                raise Exception("Disconnection failed. Please connect to the server first.")
            self.socket.send(f'/leave {self.handle}'.encode('utf-8'))
            res = self.socket.recv(1024).decode('utf-8')
            if res == "Connection closed. Thank you!":
                self.socket.close()
                self.socket = None
                return res
            else: 
                raise Exception("Error: Disconnection failed.")
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def register_handle(self, params):
        try:
            if len(params) != 2:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.handle is not None:
                raise Exception("Already registered.")
            user_handle = params[1]
            if self.socket is None:
                raise Exception("Registration failed. Please connect to the server first.")
            self.socket.send(f'/register {user_handle}'.encode('utf-8'))
            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')
            
            if res == f"Welcome {user_handle}!":
                self.handle = user_handle
                return res
            else:
                raise Exception(res)
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def send_file_to_server(self, params):
        try:
            if len(params) != 2:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.socket is None:
                raise Exception("Cannot send file. Please connect to the server first.")
            if self.handle is None:
                raise Exception("Cannot send file. Please register first.")
            
            filename = params[1]
            dir = os.path.dirname(os.path.abspath(__file__))
            dir_files = os.listdir(dir)

            if filename not in dir_files:
                raise Exception("File not found.")
            
            self.socket.send(f"/store {self.handle} {filename}".encode('utf-8'))
            
            filename = dir + '\\' + filename
            with open(filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    self.socket.send(file_data)
                    file_data = file.read(1024)
                self.socket.send(b'<<EOF>>')
                file.close()

            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')

            if "Uploaded" in res:
                print(res)
                return res
            else:
                raise Exception(res)

        except IOError:
            errorMsg = "Error: File not found."
            print(errorMsg)
            return errorMsg
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def get_clients(self, params):
        try:
            if len(params) != 1:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.socket is None:
                raise Exception("Cannot get list of users. Please connect to the server first.")
            print("Requesting user list from server...")
            self.socket.send(("/clients").encode('utf-8'))
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def message(self, params):
        # params[0] = /msg
        # params[1] = client_name
        # params[2] = destination_client_name
        # params[3] = message
        try:
            if len(params) != 3:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.socket is None:
                raise Exception("Cannot send message. Please connect to the server first.")
            if self.handle is None:
                raise Exception("Cannot send message. Please register first.")
            
            destination_client_name = params[1]
            message = params[2]

            self.socket.send(f"/msg {self.handle} {destination_client_name} {message}".encode('utf-8'))
            res = self.socket.recv(1024).decode('utf-8')

            if res == "Message sent.":
                print(res)
                return res
            else:
                raise Exception(res)
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def receive(self):
        pass
        
    def message_all(self, params):
        pass
    
    def request_directory_list(self, params):
        try:
            if len(params) != 1:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.socket is None:
                raise Exception("Cannot check file directory. Please connect to the server first.")
            if self.handle is None:
                raise Exception("Cannot check file directory. Please register to the server first.")
            self.socket.send(("/dir").encode('utf-8'))
            res = self.socket.recv(1024).decode('utf-8')
            return res
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def fetch_file_from_server(self, params):
        try:
            if len(params) != 2:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.socket is None:
                raise Exception("Cannot send file. Please connect to the server first.")
            if self.handle is None:
                raise Exception("Cannot send file. Please register first.")
            
            filename = params[1]

            self.socket.send(f"/get {filename}".encode('utf-8'))

            dir = os.path.dirname(os.path.abspath(__file__))
            dir_files = os.listdir(dir)
            
            if filename in dir_files:
                i = 1
                actual_file = filename.split('.')

                if isinstance(actual_file, list):
                    filename = ''
                    for j in range(len(actual_file) - 1):
                        filename += actual_file[j]
                        if j != len(actual_file) - 2:
                            filename += '.'

                    while (f'{filename}-{i}.{actual_file[-1]}') in dir_files:
                        i += 1
                    filename = f'{filename}-{i}.{actual_file[-1]}'
                else:
                    filename = actual_file
                    while (f'{filename}-{i}') in dir_files:
                        i += 1
                    filename = f'{filename}-{i}'
            
            with open(filename, 'wb') as file:
                while True:
                    file_data = self.socket.recv(1024)
                    if b'<<EOF>>' in file_data:
                        break
                    file.write(file_data)
                print('done reading')
                file.close()
            
            res = self.socket.recv(1024).decode('utf-8')

            if "File received from Server: " in res:
                print(f"File received from Server: {filename}")
                return f"File received from Server: {filename}"
            else:
                raise Exception(res)
        
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def show_commands(self, params):
        msg = msg = "----------------------\n|| COMMANDS ||\n- "
        for command in self.commands:
            msg += f"{self.commands[command]['usage']} - {self.commands[command]['desc']}\n"
        msg += "\n----------------------\n"
        print(msg)
        return msg

if __name__ == "__main__":
    client = Client()
    client.root.mainloop()