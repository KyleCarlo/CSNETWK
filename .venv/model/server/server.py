#import socket module
from socket import *

# import thread module
import threading

# import sys for termination
import sys # In order to terminate the program

class Server:
    def __init__(self):
        self.serverPort = 12345
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen()
        self.commands = {
            "/join": {
                "desc": "Connect to the server application",
                "usage": "/join <server_ip_add> <port>",
                "call": None
            }, 
            "/leave": {
                "desc": "Disconnect from the server application",
                "usage": "/leave",
                "call": None
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
                "call": None
            }
        }

        while True:
            #Establish the connection
            print('CSNETWK Web Server is ready to serve...')
            
            try:
                connectionSocket, addr = self.serverSocket.accept()
                thread = threading.Thread(target=self.handle_client, args=(connectionSocket, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            
            except IOError:
                #Send response message for file not found
                response = 'ERROR'
                connectionSocket.send(response.encode('utf-8'))
            
                #Close client socket
                connectionSocket.close()

    def handle_client(self, connectionSocket, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        # connected = True
        # while connected: 
        #     msg = connectionSocket.recv(1024).decode('utf-8')
        #     print(f"[{addr}] {msg}")
        #     reply = f"HELLO {addr}"
        #     connectionSocket.send(reply.encode('utf-8'))
        #     print(msg)

server = Server()