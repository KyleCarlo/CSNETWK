"""
    Client Class and Methods
"""
# Import libraries
import socket
import tkinter as tk
from tkinter import scrolledtext, Entry, Button
import os
import threading
class Client:
    # Initialize the server
    def __init__(self):
        # Initialize the client's handle
        self.handle = None
        # Initialize the client's socket
        self.socket = None
        # Initialize a separate socket for messaging
        self.message_socket = None
        # Define the dictionary of commands with description, usage, and method to call
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
            "/pm": {
                "desc": "Message another registered client connected to the server",
                "usage": "/pm <client_name> <message>",
                "call": self.message
            },
            "/all": {
                "desc": "Message other registered clients connected to the server",
                "usage": "/all <message>",
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
        self.root.title("File Exchange System")
        
        # GUI for the console
        self.output_text = scrolledtext.ScrolledText(self.root, width=70, height=20, state='disabled')
        self.output_text.grid(row=0, column=0, padx=10, pady=10)

        # GUI for the chat room
        self.chat_room = scrolledtext.ScrolledText(self.root, width=50, height=20, state='disabled')
        self.chat_room.grid(row=0, column=1, padx=10, pady=10)

        # GUI for the command entry and send button
        self.input_entry = Entry(self.root, width=70)
        self.input_entry.grid(row=1, columnspan=2, pady=5)
        self.send_button = Button(self.root, text="Send", command=self.send_user_input)
        self.send_button.grid(row=2, columnspan=2, pady=(5, 10))
        self.send_button.bind(func=self.send_user_input, sequence="<Return>")

    # Sends user input to the server
    def send_user_input(self, event=None):
        # Get the input from the console
        command = self.input_entry.get()
        
        try:
            # Check if the command is valid and separate the command arguments
            isValid, args = self.check_command(command)

            # If the command is valid, call the method associated with the command
            if isValid: 
                res = self.commands[args[0]]["call"](args) # Call the command's method

                # Display the response to GUI's console
                self.output_text.configure(state='normal')
                self.output_text.insert(tk.END, f"{res}\n") 
                self.output_text.configure(state='disabled')

                # Clear the input field if the command is valid
                if 'Error:' not in res:
                    self.input_entry.delete(0, tk.END)
            else: 
                raise Exception("Command not found.")

        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            self.output_text.configure(state='normal')
            self.output_text.insert(tk.END, f"{errorMsg}\n")
            self.output_text.configure(state='disabled')

    # Method to check if the command is valid
    def check_command(self, params):
        # Check if there are parameters
        if len(params) == 0:
            return False, None
        
        # Split the received parameters into arguments
        args = params.split(" ")
        # If there is only 1 parameter, place it in a list
        if isinstance(args, str):
            args = [args]

        # Check if the first argument is a valid command
        # Return the arguments passed
        if args[0] in self.commands.keys():
            return True, args
        
        # Returns False if command is invalid
        return False, None
    
    # Method to connect to the server
    def connect_to_server(self, params):
        try:
            # Check that there are exactly 3 parameters and that the third param is numerical
            if len(params) != 3 or not params[2].isdigit(): 
                raise Exception("Command parameters do not match or is not allowed.")
            # Check that there is already an existing socket
            if self.socket is not None:
                raise Exception("Connection to the Server is already established.")
            
            # Save the server host name and port number
            server_host = params[1]
            server_port = int(params[2])
            # Initialize the general socket and messaging socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect both the general socket and messaging socket
            try:
                self.socket.connect((server_host, server_port))
                self.message_socket.connect((server_host, server_port))
            except:
                raise ConnectionError
            # Return a response indicating successful connection
            msg = "Connection to the File Exchange Server is successful!"
            print(msg)
            return msg
        
        except ConnectionResetError:
            # Print error
            errorMsg = f"Error: Connection to the Server has been reset."
            print(errorMsg)
            self.output_text.configure(state='normal')
            self.output_text.insert(tk.END, f"{errorMsg}\n")
            self.output_text.configure(state='disabled')

        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg
        
    # Method to disconnect from the server
    def disconnect_from_server(self, params):
        try:
            # Check that there is exactly 1 parameters
            if len(params) != 1: 
                raise Exception("Command parameters do not match or is not allowed.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Disconnection failed. Please connect to the server first.")
            
            # Send the disconnect command to the server
            self.socket.send(f'/leave {self.handle}'.encode('utf-8'))
            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')

            # Check if the server has successfully disconnected
            if res == "Connection closed. Thank you!":
                # Close the sockets and set them to None
                self.socket.close()
                self.message_socket.close()
                self.socket = None
                self.message_socket = None
                self.handle = None
                return res
            else: 
                raise Exception("Error: Disconnection failed.")
            
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    # Method to register a handle
    def register_handle(self, params):
        try:
            # Check that there are exactly 2 parameters
            if len(params) != 2:
                raise Exception("Command parameters do not match or are not allowed.")
            # Check that the client is already registered
            if self.handle is not None:
                raise Exception("Already registered.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Registration failed. Please connect to the server first.")
            
            # Save the user handle
            user_handle = params[1]
            # Send the register command to the server
            self.socket.send(f'/register {user_handle}'.encode('utf-8'))

            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')
            
            # Check if the server has successfully registered the handle
            if res == f"Welcome {user_handle}!":
                self.handle = user_handle
                # Start a thread to listen for messages
                threading.Thread(target=self.receive).start()
                return res
            else:
                raise Exception(res)
            
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
            
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    # Method to send a file to the server
    def send_file_to_server(self, params):
        try:
            # Check that there is exactly 2 parameters
            if len(params) != 2:
                raise Exception("Command parameters do not match or are not allowed.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Cannot send file. Please connect to the server first.")
            # Check that the client is already registered
            if self.handle is None:
                raise Exception("Cannot send file. Please register first.")
            
            # Save the filename
            filename = params[1]
            # Get the current directory and files inside
            dir = os.path.dirname(os.path.abspath(__file__))
            dir_files = os.listdir(dir)

            # Check that requested file is in the directory
            if filename not in dir_files:
                raise Exception("File not found.")
            
            # Send the storing command to the server
            self.socket.send(f"/store {self.handle} {filename}".encode('utf-8'))
            
            # Reading the file
            with open(dir + '\\' + filename, 'rb') as file:
                # Read the initial 1024 bits
                file_data = file.read(1024)
                while file_data:
                    # Send the chunks to the socket and continue reading
                    self.socket.send(file_data)
                    file_data = file.read(1024)
                # Send tht EOF tag to the socket
                self.socket.send(b'<<EOF>>')
                # Close the file
                file.close()

            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')

            # Check if response from server is OK and print as follows
            if "Uploaded" in res:
                print(res)
                return res
            else:
                raise Exception(res)
            
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg

        except IOError:
            # Catch any IO errors
            errorMsg = "Error: File not found."
            print(errorMsg)
            return errorMsg
        except Exception as e:
            # Print other errors
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg    
    
    # Method to request the directory list from the server
    def request_directory_list(self, params):
        try:
            # Check that the number of parameters is exactly 1
            if len(params) != 1:
                raise Exception("Command parameters do not match or are not allowed.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Cannot check file directory. Please connect to the server first.")
            # Check that the client is already registered
            if self.handle is None:
                raise Exception("Cannot check file directory. Please register to the server first.")
            # Send the directory command to the server
            self.socket.send(("/dir").encode('utf-8'))
            # Receive the response from the server
            res = self.socket.recv(1024).decode('utf-8')
            # Check if the server has successfully sent the directory list
            if "SERVER DIRECTORY" in res:
                print(res)
                return res
            else:
                raise Exception(res)
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    # Method to fetch a file from the server
    def fetch_file_from_server(self, params):
        try:
            # Check that the number of parameters is exactly 2
            if len(params) != 2:
                raise Exception("Command parameters do not match or are not allowed.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Cannot fetch file. Please connect to the server first.")
            # Check that the client is already registeref
            if self.handle is None:
                raise Exception("Cannot fetch file. Please register first.")
            
            # Save the filename
            filename = params[1]
            # Send the get file command to the server
            self.socket.send(f"/get {filename}".encode('utf-8'))
            # Get the current directory and files inside
            dir = os.path.dirname(os.path.abspath(__file__))
            dir_files = os.listdir(dir)
            
            # Logic for appending -n to the nth version of the file with the same name
            if filename in dir_files:
                i = 1
                actual_file = filename.split('.')
                # Add a number to the end of the filename
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

            proceed = self.socket.recv(1024).decode('utf-8')
            if proceed != "Proceed to receive.":
                raise Exception(proceed)
            
            # Writing the file data to the newly created file
            with open(dir + '\\' + filename, 'wb') as file:
                while True:
                    # Get 1024 bits of data at a time
                    file_data = self.socket.recv(1024)
                    # If last chunk of data, write but excluding the EOF tag
                    if b'<<EOF>>' in file_data:
                        break
                    # Write to the file
                    file.write(file_data)
                # Close the file
                file.close()
            
            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')

            # Check if the server has successfully sent the file
            if "File received from Server: " in res:
                print(f"File received from Server: {filename}")
                return f"File received from Server: {filename}"
            else:
                raise Exception(res)
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

    # Method to show the list of commands
    def show_commands(self, params):
        # Print the list of commands with formatting
        msg = msg = "----------------------\n|| COMMANDS ||\n"
        for command in self.commands:
            msg += f"{self.commands[command]['usage']} - {self.commands[command]['desc']}\n"
        msg += "\n----------------------\n"
        print(msg)
        return msg
    
    # Method for the client to message another client
    def message(self, params):
        try:
            # Check that there are at least 3 parameters
            if len(params) < 3:
                raise Exception("Command parameters do not match or are not allowed.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Cannot send message. Please connect to the server first.")
            # Check that the client is already registered
            if self.handle is None:
                raise Exception("Cannot send message. Please register first.")
            
            # Save the destination client's handle
            destination_client_name = params[1]
            # Save the message, allowing messages with spaces by connecting the words
            message = " ".join(params[2:])
            # Send the message command to the server
            self.socket.send(f"/pm {self.handle} {destination_client_name} {message}".encode('utf-8'))
            
            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')
            
            # Check if the server has successfully sent the message
            if "Message sent" in res:
                print(res)
                return res
            else:
                raise Exception(res)
            
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg
        
    # Method for the client to message all other clients
    def message_all(self, params):
        try: 
            # Check that there are at least 2 parameters
            if len(params) < 2:
                raise Exception("Command parameters do not match or are not allowed.")
            # Check that there is an existing socket
            if self.socket is None:
                raise Exception("Cannot send message. Please connect to the server first.")
            # Check that there is an existing handle
            if self.handle is None:
                raise Exception("Cannot send message. Please register first.")
            
            # Save the message, allowing messages with spaces by connecting the words
            message = " ".join(params[1:])
            # Send the message all command to the server
            self.socket.send(f"/all {self.handle} {message}".encode('utf-8'))
            
            # Receive the server's response
            res = self.socket.recv(1024).decode('utf-8')
            # Check if the server has successfully sent the message
            if res == "Message sent to all other clients.":
                print(res)
                return res
            else:
                raise Exception(res)
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg
        except Exception as e:
            # Print error
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg
        
    # Method for the client to receive messages
    def receive(self):
        # Continuously receive messages from the server
        try:
            while True:
                message = self.message_socket.recv(1024).decode('utf-8')

                if ":" not in message:
                    message = "[DISCONNECTED]."
                    print(message)
                    break
                # Display the message to the GUI's console
                self.chat_room.configure(state='normal')
                self.chat_room.insert(tk.END, f"{message}\n")
                self.chat_room.configure(state='disabled')
                print(message)
        except ConnectionError:
            # Check for possible connection errors
            # Set the sockets to None for safety
            self.socket = None
            self.message_socket = None
            # Print error
            msg = f"Error: Connection to the Server has failed! Please check IP Address and Port Number."
            print(msg)
            return msg

# Main method
if __name__ == "__main__":
    # Instantiate the client 
    client = Client()
    # Start the GUI
    client.root.mainloop()