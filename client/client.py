# In client.py
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog  # Added simpledialog
import os
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
        # self.output_text.insert(tk.END, f"User Input: {command}\n")
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
# with open(filename, 'rb') as file:
    
#     # self.client_socket.send(f"/store {filename}".encode('utf-8'))  # Start of file transmission

#     file_data = file.read(1024)
#     while file_data:
#         self.client_socket.send(file_data)
#         file_data = file.read(1024)

#     # Add an end-of-file marker
#     self.client_socket.send(b'<<EOF>>')

        except IOError:
            errorMsg = "Error: File not found."
            print(errorMsg)
            return errorMsg
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg
        # try:
        #     with open(filename, "rb") as file:
        #         file_data = file.read()
        #         file_size = len(file_data)

        #         # Send the command to the server
        #         self.send_message(f"/store {filename}")

        #         # Receive the server's acknowledgment
        #         acknowledgment = self.server_socket.recv(1024).decode("utf-8")

        #         if acknowledgment.startswith("Ready to receive"):
        #             # Send the file data to the server
        #             self.server_socket.sendall(file_data)

        #             # Display success message with timestamp
        #             timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        #             self.display_output(f"{self.handle}<{timestamp}>: Uploaded {filename}")
        #         else:
        #             self.display_output(f"Server rejected the file: {acknowledgment}")
        # except FileNotFoundError:
        #     self.display_output(f"Error: File '{filename}' not found.")
        # except Exception as e:
        #     self.display_output(f"Error: {e}")
    def message(self, params):
        pass
        
    def message_all(self, params):
        pass

    def request_directory_list(self, params):
        # Implement directory list request logic
        # try:
        #     # Send the command to the server
        #     self.send_message("/dir")

        #     # Receive the server's response
        #     server_response = self.server_socket.recv(1024).decode("utf-8")

        #     if server_response.startswith("Server Directory"):
        #         # Display the server directory list
        #         directory_list = server_response.split("\n")[1:]
        #         self.display_output("Server Directory\n" + "\n".join(directory_list))
        #     else:
        #         self.display_output(f"Error: {server_response}")

        # except Exception as e:
        #     self.display_output(f"Error: {e}")
        try:
            if len(params) != 1:
                raise Exception("Command parameters do not match or are not allowed.")
            if self.socket is None:
                raise Exception("Cannot check file directory. Please connect to the server first.")
            self.socket.send("/dir".encode('utf-8'))
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    def fetch_file_from_server(self, filename):
        # Implement file fetching logic
        self.send_message(f"/get {filename}")

    def show_commands(self, params):
        msg = ""
        for command in self.commands:
            msg += f"{self.commands[command]['usage']} - {self.commands[command]['desc']}\n"
        self.output_text.insert(tk.END, f"{msg}\n")

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