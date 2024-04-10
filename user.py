import socket as socket
import util
"""
User object for ip addr, port numbers, and username
"""
class User:

    def __init__(self, ip = 'localhost', port = 8080, username = 'default'):
        self.ip = ip
        self.port = port
        self.username = f'[{username}]:~$'
        self.socket = None
        self.connection = None
        self.address = None


    @util.threaded
    def start_server(self, connection_event):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.ip, self.port))
            server_socket.listen()
            
            self.connection, self.address = server_socket.accept()
            connection_event.set()  # Signal that a connection has been made

    def find_server():
        pass
        

    # Return a string representation of the User.username
    def __repr__(self):
        return f'{self.username}'
    def __str__(self):
        return f'{self.username}'