import socket as socket


class User:
    """
    A class representing a User in a networked chat application.
    This class handles network connection settings and state, such as IP address, port number, and username.
    It also manages the socket for network communications.
    """
    def __init__(self, ip = 'localhost', port = 8080, username = 'default'):
        """
        Initialize a new User instance.
        
        Args:
            ip (str): The IP address where the user will host or connect. Defaults to 'localhost'.
            port (int): The network port on which the user will host or connect. Defaults to 8080.
            username (str): The username of the user. This will be used in the chat display.
        """
        self.ip = ip
        self.port = port
        self.username = f'[{username}]:~$' # Format the username as it might appear in a terminal.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a new http socket.
        
    # Return a string representation of the User.username
    def __str__(self):
        """
        Return a string representation of the User's username.
        
        Returns:
            str: The formatted username.
        """
        return f'{self.username}'
    
    def __len__(self):
        """
        Return the length of the username for any length-based operations.
        
        Returns:
            int: The length of the formatted username.
        """
        return len(self.username)

    def listening(self):
        """
        Set up the user's socket to listen for incoming connections.
        This method configures the socket to bind to the specified IP address and port number,
        and starts listening for incoming connections.
        """
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1) # The socket is configured to allow only one incoming connection.

    def searching(self):
        """
        Prepare to connect to a server by returning the server address.
        
        Returns:
            tuple: A tuple containing the IP address and port number for connecting to a server.
        """
        server_addr = (self.ip, self.port)
        return server_addr