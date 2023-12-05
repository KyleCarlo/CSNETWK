# In server.py
from socket import *
import threading
from datetime import datetime
import os

class Server:
    # Initializing the server 
    def __init__(self):
        # Set port to 12345
        self.serverPort = 12345
        # Create a server socket and bind it to the localhost and port
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('127.0.0.1', self.serverPort))
        # Start listening for connections
        self.serverSocket.listen()
        # Initialize a dictionary to store clients
        self.clients = {} # key: handle, values: (socket, address)
        # Define the list of commands with description, usage, and method to call
        self.commands = {
            "/leave": {
                "desc": "Disconnect from the server application",
                "usage": "/leave",
                "call": self.disconnect_client
            }, 
            "/register": {
                "desc": "Register a unique handle or alias",
                "usage": "/register <handle>",
                "call": self.register_handle
            },
            "/store":{
                "desc": "Send file to server",
                "usage": "/store <handle> <filename>",
                "call": self.store_file
            }, 
            "/dir": {
                "desc": "Request directory file list from a server",
                "usage": "/dir",
                "call": self.get_dir
            }, 
            "/get":{
                "desc": "Fetch a file from a server",
                "usage": "/get <filename>",
                "call": self.get_file
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
            }
        }

        # Keep listening for connections
        while True:
            print('CSNETWK Web Server is ready to serve...')
            
            try:
                # Accept an incoming connection
                connectionSocket, addr = self.serverSocket.accept()
                # Create a thread to handle the client
                thread = threading.Thread(target=self.handle_client, args=(connectionSocket, addr))
                thread.start()
                # Display number of active connections
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
            except IOError:
                # TODO:IDK WHAT TO DO HERE
                print("Error: Multithreading Error...")

    # Method to handle client connections
    def handle_client(self, connectionSocket, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        while True:
            try:
                # Receive data from the client
                data = connectionSocket.recv(1024).decode('utf-8')
                
                if not data:
                    # Empty string received, client disconnected
                    print(f"[DISCONNECTED] {addr} disconnected.")
                    break

                # Split the received data to be saved as a list
                command = data.split(' ')
                if isinstance(command, str):
                    args = [command]
                elif isinstance(command, list):
                    args = command

                # If /register, append the client socket and address for later
                if args[0] == '/register':
                    args.append(connectionSocket)
                    args.append(addr)

                # If /store or /get, append the client socket for later
                if args[0] == '/store' or args[0] == '/get':
                    args.append(connectionSocket)

                # Call the corresponding method based on the args
                # Store the response
                res = self.commands[args[0]]["call"](args)

                # Send the response to the client socket
                connectionSocket.send(res.encode('utf-8'))

            except Exception as e:
                # Print the error
                print(f"Error: {str(e)}")
                break
    
    # Method to register the alias of the client
    def register_handle(self, params):
        try:
            # Check if the handle is already existing
            if params[1] in self.clients.keys():
                raise Exception("Registration failed. Handle or alias already exists.")
            # Saving the client to the dictionary of clients
            self.clients[params[1]] = {"socket" : params[2], "address" : params[3]}
            # Return a response to indicate successful registration
            return f"Welcome {params[1]}!"
        except Exception as e:
            # Print the error
            errorMsg = f"{e}"
            print("Error:", errorMsg)
            return errorMsg

    # Method to disconnect the client from the server
    def disconnect_client(self, params):
        try:
            # Delete the client from the list of clients if registered
            if params[1] is not None and params[1] in self.clients.keys():
                del self.clients[params[1]]
            # Return a response to indicate succesful disconnection
            return "Connection closed. Thank you!"
        except Exception as e:
            # Print the error
            errorMsg = f"{e}"
            print("Error:", errorMsg)
            return errorMsg

    # Method to store a file sent by the client to the server
    def store_file(self, params):
        try:
            # Save client socket and filename as variables
            connectionSocket = params[3]
            filename = params[2]
            # Get the current directory and files inside
            dir = os.path.dirname(os.path.abspath(__file__))
            dir_files = os.listdir(dir)

            # Create the folder 'server_files' to save the files
            if 'server_files' not in dir_files:
                os.mkdir(dir + '/server_files')

            # Get the list of files in the 'server_files' folder
            dir_files = os.listdir(dir + '\\server_files')
            
            # Logic for appending -n to the nth version of the file with the same name
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
            
            # Writing the file data to the newly created file
            with open(dir + '\\server_files\\' + filename, 'wb') as file:
                while True:
                    # Get 1024 bits of data at a time
                    data = connectionSocket.recv(1024)
                    # If last chunk of data, write but excluding the EOF tag
                    if b"<<EOF>>" in data:
                        file.write(data[:-7])
                        break
                    # Write to the file
                    file.write(data)                
                file.close()

            # Return a response indicating succesful storage of file in server
            msg = f"{params[1]} <{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}>: Uploaded {filename}"
            print(msg)
            return msg
        except Exception as e:
            # Print the error
            errorMsg = f"{e}"
            print("Error:", errorMsg)
            return errorMsg
    # Method to get the directory of files stored in the server
    def get_dir(self, params):
        try:
            # Getting the path to the 'server_files' folder
            dir = os.path.dirname(os.path.abspath(__file__)) + '\\server_files'
            # Getting the list of files in the directory
            dir_files = os.listdir(dir)
            
            # Preparing the message to be returned as response
            msg = "----------------------\n|| SERVER DIRECTORY ||\n- " 
            # Iterating through the files and adding the filenames to the response
            for i in range(len(dir_files)):
                msg += dir_files[i] + ('\n- ' if i != len(dir_files) - 1 else '')
            msg += "\n----------------------\n"
            # Return the response containing the files and indicating successful directory getting
            return msg
        except Exception as e:
            # Print the error
            errorMsg = f"{e}"
            print("Error:", errorMsg)
            return errorMsg
    
    # Method to get the list of other clients
    def get_clients(self, params):
        # Get the list of clients
        clients = self.clients.keys()
        # Remove requesting client from list
        clients.remove(params[1])
        # Return list of other clients, indicating successful retrieval
        return clients
    
    # 
    def message(self, params): 
        try:
            source_name = params[1]
            dest_name = params[2]
            msg = params[3]
            if dest_name not in self.clients.keys():
                raise Exception("Client not found in the server")
            dest_socket = self.clients[dest_name]["socket"]
            dest_socket.send(f"{source_name}: {msg}".encode('utf-8'))

            msg = "Message sent."
            print(msg)
            return msg
        except Exception as e:
            errorMsg = f"{e}"
            print("Error:", errorMsg)
            return errorMsg

    def message_all(self, params): pass

    def get_file(self, params): 
        try:
            connectionSocket = params[2]
            filename = params[1]
            dir = os.path.dirname(os.path.abspath(__file__))
            dir_files = os.listdir(dir)

            if 'server_files' not in dir_files:
                raise Exception("No files in the server")
            
            dir += '\\server_files'
            dir_files = os.listdir(dir)
            print(dir_files)
            print(dir)
            print(filename)

            if filename not in dir_files:
                raise Exception("File not found in the server")
            
            with open(dir + '\\' + filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    connectionSocket.send(file_data)
                    file_data = file.read(1024)
                connectionSocket.send(b"<<EOF>>")
                file.close()

            msg = f"File received from Server: {filename}"
            print(msg)
            return msg
                
        except IOError:
            errorMsg = "Error: IO ERROr."
            print(errorMsg)
            return errorMsg
        except Exception as e:
            errorMsg = f"{e}"
            print("Error:", errorMsg)
            return errorMsg
server = Server()