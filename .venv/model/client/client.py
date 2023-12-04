import socket
import sys

class Client:
    def __init__(self):
        self.server_host = None
        self.server_port = None
        self.socket = None
        self.commands = {
            "/join": {
                "desc": "Connect to the server application",
                "usage": "/join <server_ip_add> <port>",
                "call": self.connect
            }, 
            "/leave": {
                "desc": "Disconnect from the server application",
                "usage": "/leave",
                "call": self.disconnect
            }, 
            "/register": {
                "desc": "Register a unique handle or alias",
                "usage": "/register <handle>",
                "call": None
            },
            "/store":{
                "desc": "Send file to server",
                "usage": "/store <filename>",
                "call": None
            }, 
            "/dir": {
                "desc": "Request directory file list from a server",
                "usage": "/dir",
                "call": None
            }, 
            "/get":{
                "desc": "Fetch a file from a server",
                "usage": "/get <filename>",
                "call": None
            },
            "/?":{
                "desc": "List of commands", 
                "usage": "/?",
                "call": self.commands
            }
        }

    def start_console(self, command):
        try:
            isValid, args = self.check_command(command)
            if isValid: 
                return self.commands[args[0]]["call"](args)
            else: 
                raise Exception("Command not found.")
            
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(errorMsg)
            return errorMsg

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

    def connect(self, params):
        try:
            if len(params) != 3 or not params[2].isdigit(): 
                raise Exception("Command parameters do not match or is not allowed.")
            elif self.socket is not None:
                raise Exception("Connection to the Server is already established.")
            self.server_host = params[1]
            self.server_port = int(params[2])
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            self.socket.connect((self.server_host, self.server_port))
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

    def disconnect(self, params):
        try:
            if self.socket is None:
                raise Exception("Error: Disconnection failed. Please connect to the server first.")
            self.socket.close()
            self.socket = None
            msg = "Connection closed. Thank you!"
            print(msg)
            return msg
        except Exception as e:
            errorMsg = f"Error: {e}"
            print(f"Error: {e}")
            return errorMsg

    def commands(self, params):
        print('-' * 20)
        print("List of commands")
        msg = []
        for command in self.commands: 
            print(self.commands[command]['desc'])
            print(self.commands[command]['usage'])
            msg.append(command + "\n - " + self.commands[command]['desc'] + "\n - " + self.commands[command]['usage'])
        print('-' * 20)
        return 
        