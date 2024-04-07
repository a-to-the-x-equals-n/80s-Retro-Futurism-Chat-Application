import socket as s
import webbrowser
import os
from pathlib import Path


def main():

    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    os.system('cls')
    HOST = input("\n\tEnter server IP: ")
    PORT = int(input("\n\n\tEnter port number: "))

    # HOST = 'localhost'
    # PORT = 8080


    # Connect to the server
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    os.system('cls')

    try:


        print("\n\n\t[ file: 'HAL_9000.html' ]")
        filename = input("\n\tEnter filename to request: ")
        # filename = 'HAL_9000.html'

        # Send a GET request for a file
        request = f"GET /{filename} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"

        # Send request
        client_socket.sendall(request.encode())

        # Receive response
        response = client_socket.recv(4096)
       

        # Find the index of the blank line separating headers and content
        blank_line_index = response.find(b'\r\n\r\n')

        # Extract the HTML text
        html = response[blank_line_index + 4:]

        os.system('cls')
        
        filepath = ABSOLUTE_PATH / filename

        # Write the HTML content to a file
        with open(filepath, 'wb') as file:
            file.write(html)
     
        # Open the saved HTML file in a web browser
        webbrowser.open(filepath)

        print(response.decode())

    finally:

        # Close the socket
        client_socket.close()



if __name__ == "__main__":

    ABSOLUTE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))

    main()
