
"""
User object for ip addr, port numbers, and username
"""
class User:

    def __init__(self, ip = 'localhost', port = 8080, username = None):
        self.ip = ip
        self.port = port
        self.username = username

    # TODO: Implement get/set functions for ip, port, and username?

    def ip(self):
        pass
    def port(self):
        pass
    def username(self):
        pass

    # TODO: Each user will have a host server listening for other clients attemption
    # to connect/message them
    def server_init(self):
        pass
    def client_init(self):
        pass
    # Return a string representation of the User.username
    def __repr__(self):
        return f'{self.username}'
    def __str__(self):
        return f'{self.username}'