from socket import *
import threading

class Server:
    def __init__(self):
        self.serverPort = 12345
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen()
        self.clients = []

    def disconnect_client(self, connectionSocket, addr):
        client = [connectionSocket, addr]
        if client in self.clients:
            self.clients.remove(client)
            print(f"[DISCONNECTED] {addr} disconnected.")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

    def handle_client(self, connectionSocket, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        self.clients.append([connectionSocket, addr])

        while True:
            try:
                msg = connectionSocket.recv(1024).decode('utf-8').split(' ', 1)
                print(f"[{addr}] {msg}")
                if msg[0] == "/leave":
                    self.disconnect_client(connectionSocket, addr)
                    break
                if msg[0] == '/register':
                    print(msg)

            except Exception as e:
                print(f"[ERROR] {str(e)}")
                self.disconnect_client(connectionSocket, addr)
                break

if __name__ == '__main__':
    server = Server()
    while True:
        try:
            connectionSocket, addr = server.serverSocket.accept()
            thread = threading.Thread(target=server.handle_client, args=(connectionSocket, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except IOError:
            print("[ERROR] Connection failed.")