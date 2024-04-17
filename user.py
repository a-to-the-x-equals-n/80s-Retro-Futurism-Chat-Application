import socket as socket

# from loading_interface import loading

"""
User object for ip addr, port numbers, and username
"""
class User:
    
    def __init__(self, ip = 'localhost', port = 8080, username = 'default'):
        self.ip = ip
        self.port = port
        self.username = f'[{username}]:~$'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # Return a string representation of the User.username
    def __str__(self):
        return f'{self.username}'
    
    def __len__(self):
        return len(self.username)

    def listening(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)

    def searching(self):
        server_addr = (self.ip, self.port)
        return server_addr